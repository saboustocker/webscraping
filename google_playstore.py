from google_play_scraper import reviews_all, Sort
import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)
PLAY_OUT = Path("data/ai_agents_google_play_reviews.csv")

play_apps = {
    "Muse": "com.facebook.aura",
    "Grok Bot": "ai.x.grok.bot",
}

all_reviews = []
for app_name, package_id in play_apps.items():
    reviews = reviews_all(package_id, lang="en", country="us", sort=Sort.NEWEST)
    print(f"{app_name}: {len(reviews)} Google Play reviews")
    for r in reviews:
        r["app_name"] = app_name
        r["package_id"] = package_id
    all_reviews.extend(reviews)

df_new = pd.DataFrame(all_reviews)

# merge with existing file instead of overwriting it, then drop duplicate reviews
if PLAY_OUT.exists():
    df_old = pd.read_csv(PLAY_OUT)
    df_new = pd.concat([df_old, df_new], ignore_index=True)
df_play = df_new.drop_duplicates(subset="reviewId", keep="last")
df_play.to_csv(PLAY_OUT, index=False)
print("\nGoogle Play total:\n", df_play.groupby("app_name").size())