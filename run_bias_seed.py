import json
from app import database, models
from sqlalchemy.orm import Session
from app.database import Base, engine

# ✅ Ensure tables are created
Base.metadata.create_all(bind=engine)

db: Session = database.SessionLocal()

with open("app/bias_data.json") as f:
    bias_data = json.load(f)

for entry in bias_data:
    if not db.query(models.NewsSource).filter_by(name=entry["name"]).first():
        source = models.NewsSource(
            name=entry["name"],
            url=entry["url"],
            bias_label=entry["bias_label"]
        )
        db.add(source)

db.commit()
db.close()
