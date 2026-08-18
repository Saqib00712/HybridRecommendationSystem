Hybrid Recommendation System

An agentic AI-powered learning platform that tracks user behavior in real time and generates personalized, persuasive course recommendations using hybrid vector + keyword search, Mesh API, and a structured multi-step AI agent workflow.

What This Project Does

Most recommendation systems use simple collaborative filtering — "users like you also bought X." This system goes further by watching what each user actually does, analyzing their interests with an AI agent, and writing custom persuasive messages for every recommendation.

User visits platform
        ↓
Behavior tracked — views, searches, scroll depth, time spent
        ↓
AI Agent triggers after 3 views OR 2 searches
        ↓
5-step agent workflow analyzes interests
        ↓
Hybrid retrieval — ChromaDB semantic search + SQL keyword fallback
        ↓
Re-ranked by category match, time spent, tags, difficulty
        ↓
Mesh API LLM writes personalized persuasive message
        ↓
Real-time recommendation delivered to user dashboard
Demo

User behavior: Viewed 3 Python courses, searched "machine learning", spent 4 minutes on a Deep Learning course

AI Agent output:

Based on your deep interest in Python and machine learning,
I noticed you spent significant time on Deep Learning foundations.
Here are 5 courses handpicked for your learning path:

1. Deep Learning Specialization — perfect next step from your Python base
2. Neural Networks from Scratch — matches your hands-on learning style
3. ML Engineering with Python — aligns with your 4 searches this week
...

Not a template. Written by the LLM for this specific user based on their actual behavior.

Architecture
User Browser
      ↓
FastAPI Backend
      ├── SQLite + SQLAlchemy  — users, products, behaviors, recommendations
      ├── ChromaDB             — 384-dim real embeddings (sentence-transformers)
      └── AI Agent Workflow:
            ↓
            Step 1: Load Activity      — last 20 user behaviors
            ↓
            Step 2: Analyze Interests  — extract categories, tags, time spent
            ↓
            Step 3: Hybrid Retrieval
                     ├── Same category products   (highest priority)
                     ├── Top interested categories
                     ├── ChromaDB semantic search (384-dim vectors)
                     └── SQL keyword search       (fallback)
            ↓
            Step 4: Re-rank            — score by category, time, tags, difficulty
            ↓
            Step 5: Generate           — Mesh API LLM writes persuasive message
            ↓
      LangSmith traces every step (timing, inputs, outputs)
      APScheduler sends daily email digest at 3PM UTC
Features
Core
JWT Authentication — Admin and User roles with bcrypt password hashing
Product CRUD — dual-write to SQLite and ChromaDB simultaneously
Behavioral event tracking — views, searches, scroll depth, time spent per product
Event batching — batches 5 events or flushes every 3 seconds
Throttling — max 1 scroll event per second to prevent noise
Hybrid search — ChromaDB semantic vector search + SQL keyword fallback
Mesh API integration — all LLM calls routed through Mesh API
Real-time updates — recommendations refresh automatically as behavior changes
Bonus Features
Structured Agent Workflow — 5-step LangGraph-style pipeline with full tracing
LangSmith Observability — every agent step traced with timing and I/O
Smart Re-ranking — scored by time spent, category match, tags, difficulty level
Hybrid Retrieval — ChromaDB semantic + SQL keyword combined scoring
Time Spent Tracking — records exact viewing duration per product
Scheduled Email Digest — APScheduler daily recommendations at 3PM UTC
Real Embeddings — 384-dim sentence-transformers (not hash-based approximations)
AI Agent — Step by Step
TRIGGER: User views 3+ products OR performs 2+ searches
         ↓
STEP 1 — Load Activity
         Fetch last 20 user behavioral events from SQLite
         ↓
STEP 2 — Analyze Interests
         Extract top categories, tags, and time-weighted signals
         ↓
STEP 3 — Hybrid Retrieval
         ├── Priority 1: Same category as top interest
         ├── Priority 2: Related categories
         ├── Priority 3: ChromaDB semantic search (384-dim cosine similarity)
         └── Priority 4: SQL keyword search fallback
         ↓
STEP 4 — Re-rank Results
         Score by: category match + time spent weight + tag overlap + difficulty fit
         ↓
STEP 5 — Generate Recommendation
         Mesh API (tencent/hy3) writes personalized persuasive message
         ↓
OUTPUT: 1 personalized message + 5 ranked product recommendations
         ↓
LangSmith logs: step timing, inputs, outputs, token usage
Tech Stack

Show Image Show Image Show Image Show Image Show Image

Category	Technology
Backend	FastAPI (Python)
Database	SQLite + SQLAlchemy ORM
Vector DB	ChromaDB (384-dim embeddings)
AI / LLM	Mesh API (tencent/hy3)
Embeddings	sentence-transformers (all-MiniLM-L6-v2)
Agent Workflow	Custom LangGraph-style structured pipeline
Scheduler	APScheduler (daily email digest)
Observability	LangSmith (step-level tracing)
Frontend	Bootstrap 5 + Jinja2 + Vanilla JS
Auth	JWT + bcrypt
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
│   ├── routers/                       # API endpoint handlers
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
LANGSMITH_API_KEY=your_langsmith_key_here   # optional — for tracing
SMTP_USER=your_email@gmail.com              # optional — for email digest
SMTP_PASSWORD=your_email_password           # optional
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
Environment Variables
Variable	Required	Description
MESH_API_KEY	✅ Yes	Mesh API key for all LLM calls
SECRET_KEY	✅ Yes	JWT token signing key
LANGSMITH_API_KEY	Optional	LangSmith observability tracing
SMTP_USER	Optional	Gmail for daily email digest
SMTP_PASSWORD	Optional	Gmail app password
Key Metrics
Metric	Value
Products	50 courses across 12 categories
Embedding dimensions	384 (all-MiniLM-L6-v2)
Vector search speed	< 100ms
Mesh API response time	~9 seconds
Total agent pipeline time	~10 seconds
Behaviors tracked	69+ events
Recommendations generated	66+
Key Concepts Covered
Behavioral tracking — event batching, throttling, time-spent weighting
Dual-write architecture — keeping SQLite and ChromaDB in sync on every product change
Hybrid retrieval — combining dense vector search and sparse keyword search
Re-ranking — multi-signal scoring beyond raw similarity distance
Structured agent workflow — LangGraph-style step-by-step pipeline with observability
Mesh API integration — routing all LLM calls through a single API gateway
LangSmith tracing — monitoring every agent step in production
JWT authentication — role-based access control for admin and user roles
APScheduler — background task scheduling without Celery overhead
Built For

SmartReco Build Challenge 2026 — a hackathon focused on building production-ready agentic recommendation systems with Mesh API integration, behavioral tracking, and vector search.

Author

Muhammad Saqib

GitHub: @Saqib00712
LinkedIn: muhammad-saqib
Email: saqibkhosa649@gmail.com
Credly: 15x IBM Certified
