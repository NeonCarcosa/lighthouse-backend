import feedparser
from sqlalchemy.orm import Session
from app import database, models
from datetime import datetime, timezone
from hashlib import sha256

RSS_FEEDS = {
    "NPR": ("https://feeds.npr.org/1001/rss.xml", "CENTER"),
    "The Intercept": ("https://theintercept.com/feed/?lang=en", "LEFT"),
    "Daily Wire": ("https://www.dailywire.com/rss.xml", "RIGHT")
}

def fetch_rss_articles():
    db: Session = database.SessionLocal()
    
    for name, (url, bias) in RSS_FEEDS.items():
        print(f"Fetching RSS from {name}...")
        source = db.query(models.NewsSource).filter_by(name=name).first()
        if not source:
            source = models.NewsSource(name=name, url=url, bias_label=bias)
            db.add(source)
            db.commit()

        feed = feedparser.parse(url)
        count = 0

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            published_at = datetime.now(timezone.utc)
            hash_input = f"{source.id}:{title}:{published_at.date()}"
            unique_hash = sha256(hash_input.encode('utf-8')).hexdigest()

            existing = db.query(models.Article).filter_by(unique_hash=unique_hash).first()
            if existing:
                continue

            new_article = models.Article(
                title=title,
                summary=summary,
                url=link,
                published_at=published_at,
                source_id=source.id,
                unique_hash=unique_hash
            )
            db.add(new_article)
            count += 1

        db.commit()
        print(f"✓ Added {count} articles from {name}")

    db.close()
    print("✅ RSS ingestion complete.")

if __name__ == "__main__":
    fetch_rss_articles()
