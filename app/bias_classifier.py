from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import database, models
import torch

# Load model and tokenizer once
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForSequenceClassification.from_pretrained("bucketresearch/politicalBiasBERT")
model.eval()

LABELS = ["LEFT", "CENTER", "RIGHT"]

def classify_bias(text: str) -> str:
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs).item()
        return LABELS[predicted_class]
    except Exception as e:
        print("Bias classification error:", e)
        return "UNKNOWN"

def classify_all_articles():
    db: Session = database.SessionLocal()
    articles = db.query(models.Article).filter(
        or_(
            models.Article.bias_label == None,
            models.Article.bias_label == "UNKNOWN"
        )
    ).all()
    print(f"🔍 Classifying {len(articles)} articles...")

    for article in articles:
        content = f"{article.title}. {article.summary}"
        article.bias_label = classify_bias(content)
        print(f"🧠 {article.title[:60]}... → {article.bias_label}")

    db.commit()
    db.close()
    print("✅ Classification complete.")

if __name__ == "__main__":
    classify_all_articles()
