from app import database, models
from app.models import BiasEnum
from sqlalchemy.orm import Session

TRUSTED_SOURCES = [
    ("Fox News", "https://www.foxnews.com", BiasEnum.RIGHT),
    ("CNN", "https://www.cnn.com", BiasEnum.LEFT),
    ("The Guardian", "https://www.theguardian.com", BiasEnum.LEAN_LEFT),
    ("Wall Street Journal", "https://www.wsj.com", BiasEnum.LEAN_RIGHT),
    ("Associated Press", "https://apnews.com", BiasEnum.CENTER),
]

def seed_sources():
    db: Session = database.SessionLocal()
    for name, url, bias in TRUSTED_SOURCES:
        exists = db.query(models.NewsSource).filter_by(name=name).first()
        if not exists:
            new_source = models.NewsSource(name=name, url=url, bias_label=bias)
            db.add(new_source)
            print(f"✅ Added: {name}")
        else:
            print(f"ℹ️ Already exists: {name}")
    db.commit()
    db.close()
    print("✅ Source seeding complete.")

if __name__ == "__main__":
    seed_sources()
