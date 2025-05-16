import requests
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app import database, models
from dateutil import parser
from hashlib import sha256
from app.bias_classifier import classify_bias

load_dotenv()
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")

TRUSTED_SOURCES = {
    "Fox News": "fox-news",
    "CNN": "cnn",
    "The Guardian": "the-guardian-uk",
    "Wall Street Journal": "the-wall-street-journal",
    "Associated Press": "associated-press"
}

MAX_PAGES = 1  # Free-tier limit

def fetch_articles():
    db: Session = database.SessionLocal()
    
    for readable_name, newsapi_id in TRUSTED_SOURCES.items():
        print(f"📡 Fetching from {readable_name}...")
        source = db.query(models.NewsSource).filter_by(name=readable_name).first()
        if not source:
            print(f"⚠️ No source found in DB for: {readable_name}")
            continue

        count = 0

        for page in range(1, MAX_PAGES + 1):
            url = (
                f"https://newsapi.org/v2/top-headlines?sources={newsapi_id}"
                f"&pageSize=100&page={page}&apiKey={NEWS_API_KEY}"
            )
            response = requests.get(url)
            data = response.json()

            if data.get("status") != "ok":
                print(f"❌ Failed to fetch page {page} from {newsapi_id}: {data}")
                break

            articles = data.get("articles", [])
            if not articles:
                break

            for article in articles:
                published_at = parser.isoparse(article['publishedAt'])
                hash_input = f"{source.id}:{article['title']}:{published_at.date()}"
                unique_hash = sha256(hash_input.encode("utf-8")).hexdigest()

                if db.query(models.Article).filter_by(unique_hash=unique_hash).first():
                    continue

                bias_label = classify_bias(article.get('description', '') or article['title'])

                new_article = models.Article(
                    title=article['title'],
                    summary=article.get('description', '') or '',
                    url=article['url'],
                    published_at=published_at,
                    source_id=source.id,
                    unique_hash=unique_hash,
                    bias_label=bias_label
                )
                db.add(new_article)
                count += 1

            db.commit()
            print(f"  • Page {page}: {len(articles)} articles fetched")

        print(f"✅ Total added from {readable_name}: {count}")

    db.close()
    print("✅ Ingestion complete.")

if __name__ == "__main__":
    fetch_articles()
