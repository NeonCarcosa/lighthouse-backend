from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from . import database, models, schemas, crud

# Create tables on startup
database.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get list of articles (with limit)
@app.get("/articles", response_model=List[schemas.ArticleSchema])
def get_articles(
    limit: int = Query(100, le=200, description="Max number of articles to return (default: 100)"),
    db: Session = Depends(get_db)
):
    return crud.get_articles(db, limit=limit)

# Get a single article by ID
@app.get("/articles/{article_id}", response_model=schemas.ArticleSchema)
def get_article(article_id: UUID, db: Session = Depends(get_db)):
    article = crud.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Get all sources with bias
@app.get("/sources", response_model=List[schemas.SourceSchema])
@app.get("/biases", response_model=List[schemas.SourceSchema])  # Alias
def get_sources(db: Session = Depends(get_db)):
    return crud.get_sources(db)

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

# Stub for future clustering
@app.get("/clusters/{cluster_id}")
def get_cluster(cluster_id: int):
    return {"cluster_id": cluster_id, "status": "Not yet implemented"}
