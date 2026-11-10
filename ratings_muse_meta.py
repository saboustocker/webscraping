import pandas as pd
from openai import OpenAI
import json
import time
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

INPUT = "data/ai_agents_google_play_reviews.csv"
BATCH_IN = "data/batch_input_agents.jsonl"
OUTPUT = "data/ai_agents_reviews_classified.csv"
MIN_WORDS = 4  # reviews shorter than this ("good", "👍") are skipped to save cost; set to 0 to keep all

# 1) load
df = pd.read_csv(INPUT)
df["content"] = df["content"].fillna("").astype(str)
print(df["app_name"].value_counts())

# 2) add columns for labels
LABEL_COLS = [
    "use_cases", "unique_qualities",
    "preference_mentioned", "preference_source", "preference_description",
    "delegated_decision", "decision_type", "decision_description",
    "choice_narrowing", "narrowing_type", "narrowing_description",
]
for c in LABEL_COLS:
    df[c] = None
df["classified"] = False

# 3) schema
SCHEMA = {
    "name": "review_content_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "use_cases": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Concrete tasks/uses the reviewer describes (e.g. 'homework help', 'image generation', 'trip planning', 'companionship'). Short lowercase labels, 1-4 words. Empty if none.",
            },
            "unique_qualities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Qualities the reviewer claims the app has or that set it apart (e.g. 'fast responses', 'remembers context', 'uncensored', 'funny personality'). Short lowercase labels, 1-4 words. Empty if none.",
            },
            "preference_mentioned": {
                "type": "boolean",
                "description": "Does the review mention that the user's preference was important for the task in some form?",
            },
            "preference_source": {
                "type": "string",
                "enum": ["inferred_by_bot", "asked_by_bot", "stated_by_user", "unclear", "none"],
                "description": "How the preference came into play: the bot inferred/learned it, the bot asked for it, the user told the bot, unclear, or none.",
            },
            "preference_description": {
                "type": "string",
                "description": "Brief description of the preference and how it was handled; empty if none.",
            },
            "delegated_decision": {
                "type": "boolean",
                "description": "Does the review describe the assistant making the final decision or choice on the user's behalf?",
            },
            "decision_type": {
                "type": "string",
                "description": "Domain of the decision (e.g. 'purchase', 'food choice', 'schedule', 'wording'); empty if none.",
            },
            "decision_description": {
                "type": "string",
                "description": "Brief description of the delegated decision; empty if none.",
            },
            "choice_narrowing": {
                "type": "boolean",
                "description": "Does the review describe the assistant reducing or prefiltering options (e.g. shortlisting, comparing, summarizing alternatives, filtering by criteria) so the user has fewer choices to evaluate, while the user still makes the final decision?",
            },
            "narrowing_type": {
                "type": "string",
                "description": "Domain of the narrowed choice set (e.g. 'products', 'restaurants', 'travel options', 'recipes'); empty if none.",
            },
            "narrowing_description": {
                "type": "string",
                "description": "Brief description of how the assistant narrowed the options or reduced the effort of choosing; empty if none.",
            },
        },
        "required": [
            "use_cases", "unique_qualities",
            "preference_mentioned", "preference_source", "preference_description",
            "delegated_decision", "decision_type", "decision_description",
            "choice_narrowing", "narrowing_type", "narrowing_description",
        ],
        "additionalProperties": False,
    },
}

SYSTEM = "You perform content analysis on Google Play reviews of AI assistant apps. For each review, extract: (1) the use cases the reviewer describes; (2) qualities the reviewer claims the app has, especially ones presented as distinctive; (3) whether user preferences are mentioned, and whether the bot inferred them, asked for them, or the user stated them; (4) whether the assistant made a final decision on the user's behalf; (5) whether the assistant narrowed or prefiltered the set of options to reduce the user's effort in choosing, without making the final decision itself. Keep (4) and (5) distinct: if the assistant picks the outcome, it is a delegated decision; if it only shortlists, compares or filters and the user picks, it is choice narrowing. Only code what is explicitly stated or clearly implied in the text. Do not guess. Generic praise ('great app', 'love it') is not a use case; it may be a quality only if specific (e.g. 'accurate', 'fast'). Reviews may be in any language; always answer in English."

# 4) build .jsonl batch input — one request per row, keyed by df index
to_classify = df[df["content"].str.split().str.len() >= MIN_WORDS]
print(f"classifying {len(to_classify)} of {len(df)} reviews")

with open(BATCH_IN, "w") as f:
    for i, row in to_classify.iterrows():
        f.write(json.dumps({
            "custom_id": str(i),
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4.1-mini",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": f"App: {row['app_name']}\nReview: {row['content']}"},
                ],
                "response_format": {"type": "json_schema", "json_schema": SCHEMA},
                "temperature": 0,
            },
        }) + "\n")

# 5) upload + create batch
batch_file = client.files.create(file=open(BATCH_IN, "rb"), purpose="batch")
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)
print(f"batch created: {batch.id}")

# 6) poll until done
while True:
    batch = client.batches.retrieve(batch.id)
    print(f"status: {batch.status}  ({batch.request_counts})")
    if batch.status in ("completed", "failed", "expired", "cancelled"):
        break
    time.sleep(30)

if batch.status != "completed":
    raise RuntimeError(f"batch ended with status: {batch.status}")

# 7) download + parse results
output = client.files.content(batch.output_file_id).text
for line in output.splitlines():
    obj = json.loads(line)
    i = int(obj["custom_id"])
    if obj.get("error") or obj["response"]["status_code"] != 200:
        print(f"error on row {i}: {obj.get('error')}")
        continue
    result = json.loads(obj["response"]["body"]["choices"][0]["message"]["content"])
    for c in LABEL_COLS:
        val = result[c]
        df.at[i, c] = "; ".join(val) if isinstance(val, list) else val
    df.at[i, "classified"] = True

df.to_csv(OUTPUT, index=False)
df.to_excel("output.xlsx")
print(f"saved {OUTPUT}")

# 8) per-app summary for the five questions
def top_labels(series, n=20):
    return (series.dropna().str.split("; ").explode().str.strip()
            .loc[lambda s: s != ""].value_counts().head(n))

done = df[df["classified"]]
for app, g in done.groupby("app_name"):
    print(f"\n========== {app} (n={len(g)}) ==========")
    print("\n1) Top use cases:\n", top_labels(g["use_cases"]))
    print("\n2) Top claimed qualities:\n", top_labels(g["unique_qualities"]))
    print("\n3) Preferences mentioned:", int(g["preference_mentioned"].astype(bool).sum()))
    print(g["preference_source"].value_counts())
    print("\n4) Delegated decisions mentioned:", int(g["delegated_decision"].astype(bool).sum()))
    print(top_labels(g["decision_type"], 10))
    print("\n5) Choice narrowing mentioned:", int(g["choice_narrowing"].astype(bool).sum()))
    print(top_labels(g["narrowing_type"], 10))