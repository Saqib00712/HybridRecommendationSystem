# SmartReco AI - Behavioral AI Recommendation Platform

> 🏆 Built for **SmartReco Build Challenge 2026**  
> An AI-powered learning platform that watches user behavior and generates personalized, persuasive course recommendations using **Mesh API** and vector search.

---

## 🎯 What It Does

SmartReco AI is an **agentic recommendation system** that:

1. **Tracks user behavior** - product views (with time spent), searches, scroll depth, category visits
2. **AI Agent analyzes interests** - understands what each user cares about based on their activity
3. **Hybrid vector + keyword search** - retrieves the most relevant courses from ChromaDB
4. **Re-ranks results** - prioritizes by category match, time spent, and tag relevance
5. **Mesh API generates persuasive recommendations** - personalized AI-written messages, not templates
6. **Auto-refreshes** as user behavior changes in real-time

---

## 🏗 Architecture
User Browser → FastAPI Backend
│
├── SQLite (users, products, behaviors, recommendations)
├── ChromaDB (384-dim real embeddings)
│
└── AI Agent Workflow:
├── Load Activity
├── Analyze Interests
├── Hybrid Retrieval (Vector + Keyword)
├── Re-rank Results
└── Generate via Mesh API (LLM)
│
└── LangSmith Observability (tracing)

text

---

## ✨ Features

### Core (Required)
- [x] JWT Authentication with Admin/User roles
- [x] Product CRUD with **Dual-Write** (SQLite + ChromaDB sync)
- [x] Behavioral event tracking (views, searches, time spent)
- [x] **Event batching** - batches 5 events or 3 seconds
- [x] **Throttling** - max 1 scroll event per second
- [x] AI agent with **hybrid search** (vector + keyword)
- [x] **Mesh API integration** (all LLM calls through Mesh)
- [x] Personalized persuasive recommendations
- [x] Real-time recommendation updates

### Bonus (Highlighted)
- [x] ⭐ **Structured Agent Workflow** - Step-by-step with tracing (LangGraph-style)
- [x] ⭐ **Scheduled Email Digest** - APScheduler daily at 3PM UTC
- [x] ⭐ **LangSmith Observability** - Every agent step traced
- [x] ⭐ **Smart Re-ranking** - Based on time spent, category match, tags
- [x] ⭐ **Hybrid Retrieval** - ChromaDB semantic + SQL keyword search
- [x] ⭐ **Time Spent Tracking** - Records how long users view each product
- [x] ⭐ **Event Batching & Throttling** - Efficient, non-blocking tracking
- [x] ⭐ **Real Embeddings** - 384-dim sentence-transformers (not hash-based)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/Saqib00712/smartreco-ai.git
cd smartreco-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure .env
env
MESH_API_KEY=rsk_your_key_here
LANGSMITH_API_KEY=lsv2_your_key_here
SECRET_KEY=any-secret-key
3. Initialize Database & Seed Products
bash
python create_users.py
python seed_products.py
4. Run
bash
uvicorn app.main:app --reload
5. Open
👉 http://localhost:8000

👥 Test Accounts
Role	Username	Password
Admin	admin	admin123
User	user	user123
🛠 Tech Stack
Category	Technology
Backend	FastAPI (Python)
Database	SQLite + SQLAlchemy
Vector DB	ChromaDB
AI/LLM	Mesh API (tencent/hy3)
Embeddings	sentence-transformers (all-MiniLM-L6-v2, 384d)
Agent	Custom LangGraph-style workflow
Scheduler	APScheduler
Observability	LangSmith
Frontend	Bootstrap 5 + Jinja2 + Vanilla JS
Auth	JWT + bcrypt
📁 Project Structure
text
smartreco-ai/
├── app/
│   ├── agents/              # AI Recommendation Agent
│   │   └── recommendation_agent.py
│   ├── models/              # SQLAlchemy Models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── behavior.py
│   │   └── recommendation.py
│   ├── schemas/             # Pydantic Schemas
│   ├── routers/             # API Endpoints
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── behaviors.py
│   │   ├── recommendations.py
│   │   └── pages.py
│   ├── services/            # Business Logic
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── behavior_service.py
│   │   ├── chroma_service.py
│   │   ├── recommendation_service.py
│   │   ├── email_service.py
│   │   └── scheduler_service.py
│   ├── utils/               # Utilities
│   │   ├── security.py
│   │   ├── mesh_api.py
│   │   └── langsmith_config.py
│   └── templates/           # Jinja2 HTML
│       ├── base.html
│       ├── auth/
│       ├── user/
│       └── admin/
├── static/                  # CSS & JS
├── data/                    # SQLite + ChromaDB (gitignored)
├── requirements.txt
├── README.md
└── .gitignore
🔑 Environment Variables
Variable	Required	Description
MESH_API_KEY	✅ Yes	Mesh API key for LLM calls
SECRET_KEY	✅ Yes	JWT signing key
LANGSMITH_API_KEY	No	LangSmith tracing
SMTP_USER	No	Email for daily digest
SMTP_PASSWORD	No	Email password
🧠 How the AI Agent Works
text
TRIGGER: User views 3+ products OR searches 2+ times
         ↓
STEP 1: Load Activity - Fetch last 20 user behaviors
         ↓
STEP 2: Analyze Interests - Extract categories, tags, time spent
         ↓
STEP 3: Hybrid Retrieval:
         ├── Same category products (highest priority)
         ├── Top interested categories
         ├── ChromaDB semantic search (384-dim vectors)
         └── SQL keyword search (fallback)
         ↓
STEP 4: Re-rank - Score by category match, time spent, tags, difficulty
         ↓
STEP 5: Generate - Mesh API LLM writes persuasive message
         ↓
OUTPUT: Personalized recommendation + 5 products
         ↓
LangSmith traces every step (timing, inputs, outputs)
📊 Key Metrics
Metric	Value
Products	50 courses across 12 categories
Embedding Dimensions	384
Vector Search Speed	<100ms
Mesh API Response	~9 seconds
Total Agent Time	~10 seconds
Behaviors Tracked	69+ events
Recommendations Generated	66+
📝 License
Built for SmartReco Build Challenge 2026.

👨‍💻 Author
Saqib - GitHub
