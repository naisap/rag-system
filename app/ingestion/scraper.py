# app/ingestion/scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langchain_core.documents import Document

BASE = "https://www.esa.int"

def get_esa_article_links(url, limit=10):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/News/" in href or "/Science_Exploration/" in href:
            full = href if href.startswith("http") else BASE + href
            links.add(full)

        if len(links) >= limit:
            break

    return list(links)


def get_date(soup):
    meta = soup.find("meta", {"name": "date"})
    if meta and meta.get("content"):
        return meta["content"]

    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        return time_tag["datetime"]

    return datetime.utcnow().strftime("%Y-%m-%d")


def scrape_esa_article(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.text.strip() if soup.title else "ESA article"

    content = "\n".join(
        p.get_text()
        for p in soup.find_all("p")
        if len(p.get_text()) > 80
    )

    return Document(
        page_content=content,
        metadata={
            "title": title,
            "source": url,
            "date": get_date(soup),
            "type": "ESA"
        }
    )