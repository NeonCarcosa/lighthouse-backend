from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from . import models

def get_articles(db: Session, limit: int = 100):
    return (
        db.query(models.Article)
        .order_by(models.Article.published_at.desc())
        .limit(limit)
        .all()
    )

def get_sources(db: Session):
    return db.query(models.NewsSource).all()

def get_article_by_id(db: Session, article_id: UUID) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()
