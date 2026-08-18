Hybrid Recommendation System

A full-stack agentic AI recommendation platform that tracks real user behavior and generates personalized, persuasive course recommendations using hybrid vector + keyword search, a structured 5-step AI agent, and Mesh API — built for the SmartReco Build Challenge 2026.

What This Project Does

Most recommendation systems use simple collaborative filtering. This project goes further by watching what each user actually does — time spent, searches, scroll depth — and running a structured AI agent pipeline to generate custom persuasive recommendations, not templates.

User visits platform
        ↓
Behavior tracked — views, searches, scroll depth, time spent
        ↓
AI Agent triggers after 3+ views OR 2+ searches
        ↓
5-step structured agent workflow runs
        ↓
Hybrid retrieval — ChromaDB semantic + SQL keyword combined
        ↓
Re-ranked by category match, time spent, tags, difficulty
        ↓
Mesh API LLM writes personalized persuasive message
        ↓
Real-time recommendation delivered to user dashboard
Agent Workflow — 5 Steps
Step 1 — Load Activity

Fetch last 20 user behavioral events from SQLite — views, searches, time spent per product.

Step 2 — Analyze Interests

Extract top categories, tag clusters, and time-weighted signals from behavior history.

Step 3 — Hybrid Retrieval
Priority 1: Same category as top interest
Priority 2: Related categories from interest profile
Priority 3: ChromaDB semantic search (384-dim cosine similarity)
Priority 4: SQL keyword search fallback
Step 4 — Re-rank Results

Score candidates by: category match weight + time spent signal + tag overlap + difficulty fit

Step 5 — Generate Recommendation
python
# Mesh API writes the personalized message
response = mesh_api.chat(
    model="tencent/hy3",
    messages=[
        {"role": "system", "content": "You are a personalized learning advisor..."},
        {"role": "user", "content": f"User interests: {interests}\nTop products: {products}"}
    ]
)

LangSmith traces every step — timing, inputs, outputs, token usage.

Architecture Overview
User Browser
      ↓
FastAPI Backend
      │
      ├── SQLite + SQLAlchemy   ← users, products, behaviors, recommendations
      ├── ChromaDB              ← 384-dim real embeddings (sentence-transformers)
      │
      └── AI Agent Workflow:
                ↓
          [Step 1] Load Activity       — last 20 behavioral events
                ↓
          [Step 2] Analyze Interests   — categories, tags, time weights
                ↓
          [Step 3] Hybrid Retrieval
                   ├── ChromaDB semantic search
                   └── SQL keyword fallback
                ↓
          [Step 4] Re-rank             — multi-signal scoring
                ↓
          [Step 5] Generate            — Mesh API LLM writes message
                ↓
          LangSmith traces all steps
          APScheduler sends daily email digest at 3PM UTC
Features
Core Features
JWT Authentication — Admin and User roles with bcrypt password hashing
Product CRUD — dual-write to SQLite and ChromaDB on every change
Behavioral event tracking — views, searches, scroll depth, time spent per product
Event batching — batches 5 events or flushes every 3 seconds
Throttling — max 1 scroll event per second to prevent noise
Hybrid search — ChromaDB semantic + SQL keyword combined scoring
Mesh API integration — all LLM calls routed through Mesh API (required)
Real-time updates — recommendations refresh automatically as behavior changes
Bonus Features
⭐ Structured Agent Workflow — 5-step LangGraph-style pipeline with full tracing
⭐ LangSmith Observability — every agent step traced with timing and I/O
⭐ Smart Re-ranking — scored by time spent, category match, tags, difficulty
⭐ Hybrid Retrieval — ChromaDB semantic + SQL keyword combined
⭐ Time Spent Tracking — exact viewing duration per product recorded
⭐ Scheduled Email Digest — APScheduler daily recommendations at 3PM UTC
⭐ Real Embeddings — 384-dim sentence-transformers (not hash-based)
Tech Stack

Show Image Show Image Show Image Show Image Show Image

FastAPI — async Python backend with automatic OpenAPI docs
SQLite + SQLAlchemy — relational database with ORM
ChromaDB — vector database with 384-dim real embeddings
Mesh API (tencent/hy3) — all LLM calls for recommendation generation
sentence-transformers (all-MiniLM-L6-v2) — local embedding model
LangSmith — agent step observability and tracing
APScheduler — background daily email digest scheduling
Bootstrap 5 + Jinja2 + Vanilla JS — frontend UI
JWT + bcrypt — authentication and authorization
Project Structure
hybrid-recommendation-system/
│
├── app/
│   ├── agents/
│   │   └── recommendation_agent.py    # 5-step AI agent workflow
│   ├── models/                        # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── behavior.py
│   │   └── recommendation.py
│   ├── schemas/                       # Pydantic request/response schemas
│   ├── routers/                       # FastAPI endpoint handlers
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── behaviors.py
│   │   ├── recommendations.py
│   │   └── pages.py
│   ├── services/                      # Business logic layer
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── behavior_service.py
│   │   ├── chroma_service.py
│   │   ├── recommendation_service.py
│   │   ├── email_service.py
│   │   └── scheduler_service.py
│   ├── utils/
│   │   ├── security.py               # JWT + bcrypt helpers
│   │   ├── mesh_api.py               # Mesh API client
│   │   └── langsmith_config.py       # LangSmith tracing setup
│   └── templates/                    # Jinja2 HTML templates
│       ├── base.html
│       ├── auth/
│       ├── user/
│       └── admin/
│
├── static/                           # CSS and JavaScript
├── data/                             # SQLite DB + ChromaDB (gitignored)
├── create_users.py                   # Seed admin and test users
├── seed_products.py                  # Seed 50 courses across 12 categories
├── requirements.txt
├── .env.example
└── README.md
Getting Started
1. Clone the repo
bash
git clone https://github.com/Saqib00712/hybrid-recommendation-system.git
cd hybrid-recommendation-system
2. Create virtual environment
bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up environment variables
bash
cp .env.example .env

Edit .env:

MESH_API_KEY=your_mesh_api_key_here
SECRET_KEY=any-random-secret-key
LANGSMITH_API_KEY=your_langsmith_key_here    # optional
SMTP_USER=your_email@gmail.com               # optional
SMTP_PASSWORD=your_email_password            # optional
5. Initialize database and seed data
bash
python create_users.py
python seed_products.py
6. Run the server
bash
uvicorn app.main:app --reload
7. Open in browser
http://localhost:8000
Test Accounts
Role	Username	Password
Admin	admin	admin123
User	user	user123
Key Concepts Covered
Behavioral tracking — event batching, throttling, time-spent weighting
Dual-write architecture — keeping SQLite and ChromaDB in sync on every product change
Hybrid retrieval — combining dense vector search and sparse keyword search with priority scoring
Re-ranking — multi-signal scoring beyond raw similarity distance
Structured agent workflow — LangGraph-style 5-step pipeline with LangSmith observability
Mesh API integration — routing all LLM calls through a single API gateway
APScheduler — background task scheduling for daily email digests
JWT authentication — role-based access control for admin and user roles
Key Metrics
Metric	Value
Products	50 courses across 12 categories
Embedding dimensions	384 (all-MiniLM-L6-v2)
Vector search speed	< 100ms
Mesh API response time	~9 seconds
Total agent pipeline time	~10 seconds
Behaviors tracked	69+ events
Recommendations generated	66+
Built For

This project was built for the SmartReco Build Challenge 2026 — a hackathon focused on building production-ready agentic recommendation systems with Mesh API integration, behavioral tracking, and vector search.

Related Certifications

Built applying skills from the IBM Building AI Agents and Agentic Workflows Specialization and RAG for Generative AI Applications Specialization on Coursera.

Show Image Show Image

Author

Muhammad Saqib

GitHub: @Saqib00712
LinkedIn: muhammad-saqib
Email: saqibkhosa649@gmail.com
Credly: 15x IBM Certified
