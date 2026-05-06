# app/ingestion/pipeline.py

from .scraper import get_esa_article_links, scrape_esa_article

def build_documents(seed_url, limit=10):
    links = get_esa_article_links(seed_url, limit=limit)

    docs = []
    for url in links:
        try:
            docs.append(scrape_esa_article(url))
        except Exception as e:
            print(f"Failed: {url} → {e}")

    return docs