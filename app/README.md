# 🕯️ Lighthouse Backend

A free, bias-aware news backend inspired by Ground News — built with FastAPI, PostgreSQL, and Transformers. Designed to help users explore news articles by source bias and topic.

---

## 🔧 Features

- 📰 Pulls live articles from major news sources and RSS feeds
- 🧠 Classifies bias using a fine-tuned BERT model
- 📊 Groups articles into topic clusters
- ⚡ FastAPI-powered public REST API
- 🔐 Secure .env config and scalable DB schema

---

## 🚀 API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| GET    | `/articles`          | List articles (optional `bias`)      |
| GET    | `/articles/{id}`     | Get full article by ID               |
| GET    | `/sources`           | List news sources + bias             |
| GET    | `/biases`            | Alias for `/sources`                 |
| GET    | `/clusters/{id}`     | View topic clusters (WIP)            |
| GET    | `/health`            | Healthcheck                          |

---

## 🧠 Bias Classification Model

Powered by [bucketresearch/politicalBiasBERT](https://huggingface.co/bucketresearch/politicalBiasBERT), with output labels:

- LEFT
- CENTER
- RIGHT

Articles are classified using title + summary content.

---

## ⚙️ Local Development

### Prereqs

- Python 3.10+
- PostgreSQL
- [Poetry](https://python-poetry.org/) or `venv`

### Setup

```bash
git clone https://github.com/NeonCarcosa/lighthouse-backend.git
cd lighthouse-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
psql -U postgres
# Then seed via:
python seed_sources.py
python -m app.news_ingestor
python -m app.rss_ingestor
python -m app.bias_classifier

# Run API
uvicorn app.main:app --reload

---


🌐 Frontend (Coming Soon)
The frontend (React-based) will allow users to:

Filter by bias

Explore clusters

Read full articles by source

---

📜 License
MIT — free to use and modify. Attribution encouraged, not required.

---

🙌 Contributing
Pull requests are welcome. For major changes, please open an issue first.

Made with love and a torchlight for truth 🕯️