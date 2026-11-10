from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse, parse_qs

data_links = []

def clean(link):
    if "google." in link and "/url" in link:
        qs = parse_qs(urlparse(link).query)
        link = qs.get("q", qs.get("url", [link]))[0]
    return link

def robot_check():
    if "/sorry/" in driver.current_url or driver.find_elements(By.ID, "captcha-form"):
        input("Robot check detected, solve it in the browser, then press Enter...")

driver = webdriver.Firefox()

driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+1y&sca_esv=37e421cff93e3de4&biw=1920&bih=911&sxsrf=ANbL-n7jdQO4dEC0ZLRUQoNITjCRg-Be2Q%3A1774268852366&ei=tDHBadaCFtyK9u8P1vby-QE&ved=0ahUKEwjWrLnFgraTAxVchf0HHVa7PB8Q4dUDCBE&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+1y&gs_lp=Egxnd3Mtd2l6LXNlcnAiS3NpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiAxeUia2wlQ_9cJWP_XCXACeACQAQCYASygAViqAQEyuAEDyAEA-AEBmAIAoAIAmAMAiAYBkgcAoAdasgcAuAcAwgcAyAcAgAgA&sclient=gws-wiz-serp")

input("Accept cookies / solve the robot check, then press Enter...")

while True:
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            data_links.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+2y&sca_esv=37e421cff93e3de4&biw=958&bih=816&ei=I1XBacOIO7aF9u8P8pKOYA&ved=0ahUKEwiDppCrpLaTAxW2gv0HHXKJAww4HhDh1QMIEQ&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+2y&gs_lp=Egxnd3Mtd2l6LXNlcnAiS3NpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiAyeUgAUABYAHAAeACQAQCYAQCgAQCqAQC4AQPIAQD4AQGYAgCgAgCYAwCSBwCgBwCyBwC4BwDCBwDIBwCACAA&sclient=gws-wiz-serp")

while True:
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            data_links.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+3y&sca_esv=37e421cff93e3de4&biw=958&bih=816&ei=gFXBac_8FYb_7_UPl5jb2Qk&ved=0ahUKEwjPvJfXpLaTAxWG_7sIHRfMNps4FBDh1QMIEQ&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+3y&gs_lp=Egxnd3Mtd2l6LXNlcnAiS3NpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiAzeUgAUABYAHAAeACQAQCYAQCgAQCqAQC4AQPIAQD4AQGYAgCgAgCYAwCSBwCgBwCyBwC4BwDCBwDIBwCACAA&sclient=gws-wiz-serp")

while True:
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            data_links.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+%224y%22&client=firefox-b-d&hs=s0E&sca_esv=e2250487dc351849&channel=entpr&ei=5lXBae_mLI-A9u8PlNb86AM&biw=958&bih=816&ved=0ahUKEwjv8f-HpbaTAxUPgP0HHRQrHz0Q4dUDCBE&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+%224y%22&gs_lp=Egxnd3Mtd2l6LXNlcnAiTXNpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiAiNHkiSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgBAZgCAKACAJgDAJIHAKAHALIHALgHAMIHAMgHAIAIAA&sclient=gws-wiz-serp")

while True:
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            data_links.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+%225y%22&client=firefox-b-d&hs=XLuU&sca_esv=e2250487dc351849&channel=entpr&biw=958&bih=816&ei=_lXBaYKUKcCC9u8PruLBsA4&ved=0ahUKEwiCi7WTpbaTAxVAgf0HHS5xEOYQ4dUDCBE&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22+%225y%22&gs_lp=Egxnd3Mtd2l6LXNlcnAiTXNpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiAiNXkiSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgBAZgCAKACAJgDAJIHAKAHALIHALgHAMIHAMgHAIAIAA&sclient=gws-wiz-serp")

while True:
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            data_links.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

dataframe_output = pd.DataFrame(data_links)
dataframe_output.to_csv("data/linkedin_links.csv",index=False,encoding="utf-8")

list_all = []
driver.get("https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22&sca_esv=37e421cff93e3de4&biw=1280&bih=946&ei=rWXBab73IPXF9u8PoeePeQ&ved=0ahUKEwj-ge2NtLaTAxX1ov0HHaHzIw84UBDh1QMIEQ&uact=5&oq=site%3Alinkedin.com%2Fposts+%22Institute+of+Behavioral+Science+and+Technology%22&gs_lp=Egxnd3Mtd2l6LXNlcnAiSHNpdGU6bGlua2VkaW4uY29tL3Bvc3RzICJJbnN0aXR1dGUgb2YgQmVoYXZpb3JhbCBTY2llbmNlIGFuZCBUZWNobm9sb2d5IkgAUABYAHAAeACQAQCYAQCgAQCqAQC4AQPIAQCYAgCgAgCYAwCSBwCgBwCyBwC4BwDCBwDIBwCACAA&sclient=gws-wiz-serp")

while True:
    time.sleep(1)
    robot_check()
    for a in driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]'):
        link = a.get_attribute("href")
        if link:
            link = clean(link)
            list_all.append({"link": link})
            print(link)

    try:
        driver.find_element(By.ID, "pnnext").click()
        time.sleep(3)
    except NoSuchElementException:
        break

dataframe_all = pd.DataFrame(list_all)
dataframe_all.to_csv("data/linkedin_links_all.csv",index=False,encoding="utf-8")