# CODEMENTOR AI
### *An Adaptive AI Coding Tutor*

> **"Don't immediately solve the student's problem. First help the student discover the solution."**

CodeMentor AI is an intelligent, full-stack programming tutor built to help students truly understand computer science concepts rather than passively generating copy-paste code.

---

## 🌟 Key Features

1. **3-Tier Progressive Hint System**:
   - **Level 1 (Socratic Discovery)**: Probing questions that help students discover where their logic assumption breaks down.
   - **Level 2 (Conceptual Mechanism)**: Clarifies the underlying data flow and algorithmic mechanisms.
   - **Level 3 (Code Directional Guidance)**: Concrete guidance pointing directly to loop bounds, base cases, or edge condition guards.
2. **Strict Server-Side Answer Locking**:
   - Solutions and full explanations remain locked until the student solves the problem or exhausts their 3 allowed attempts. The frontend cannot bypass this rule.
3. **Optional Onboarding Knowledge Check**:
   - Diagnostic baseline question bank with deterministic grading comparing self-declared skill vs. verified performance, generating clear gap analysis.
4. **Deterministic Learner Profile & Mastery Engine**:
   - Computes concept mastery ($0.0 - 1.0$) across Topics (Recursion, Loops, Arrays, DP, Strings, etc.), dynamically tracking recurring misconceptions (`missing_base_case`, `off_by_one`, `wrong_loop_boundary`).
5. **Personalized Problem Recommendation Engine**:
   - Scores candidate challenges based on weakness match, difficulty tier, and recent failure history with natural-language reasoning.
6. **"Revise My Mistakes" Hub**:
   - Dedicated corrective review transforming recurring mistakes into targeted remediation challenges.
7. **"Own Problem" Workspace**:
   - Open tutor mode allowing students to bring any custom problem and code for AI diagnosis and progressive tutoring.
8. **Multi-Turn Contextual AI Tutor Chat**:
   - Real-time pedagogical dialogue retaining short-term conversation context and long-term student learner profile state.

---

## 🛠️ Tech Stack

- **Backend**:
  - Python 3.14+
  - FastAPI (Async API Gateway)
  - Pydantic v2 (Data Validation & Structured Output)
  - PyMongo 4.9+ Async (`AsyncMongoClient` with built-in high-performance async in-memory fallback)
  - PyJWT & Bcrypt (Secure authentication)
- **AI & LLM**:
  - Google Gemini API (`google-genai` Python SDK)
  - Default Model: `gemini-3.7-flash` (Configurable via `GEMINI_MODEL` environment variable)
  - Strict Pydantic structured output models (`TutorAnalysis`, `ConversationReply`, `KnowledgeGapExplanation`)
  - Deterministic fallback engine for network resilience
- **Frontend**:
  - React 18 + Vite
  - Tailwind CSS + Lucide Icons
  - Monaco Code Editor (`@monaco-editor/react`)
  - React Router v6

---

## 📂 Project Structure

```
codementor-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint & lifespan
│   │   ├── core/                       # Settings (config.py) & Security (security.py)
│   │   ├── db/                         # PyMongo Async client & 16-problem Seed data
│   │   ├── models/                     # Mongo & Pydantic domain models
│   │   ├── schemas/                    # Request / Response DTO schemas
│   │   ├── routes/                     # REST endpoints (auth, problems, sessions, tutor, learner)
│   │   ├── services/                   # Business logic (tutor, learner, recommendation, assessment)
│   │   ├── ai/                         # Gemini 3.7 Flash integration, prompts, structured schemas
│   │   ├── execution/                  # Safe sandbox code runner & test evaluator
│   │   └── utils/                      # Errors & Logging
│   ├── tests/                          # 11 Unit & Integration tests (pytest)
│   ├── .env.example                    # Environment template
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                        # Typed Axios API client
│   │   ├── components/                 # Navbar, HintDrawer, SolutionModal, TutorChat, Console
│   │   ├── context/                    # AuthContext (JWT state)
│   │   ├── pages/                      # Dashboard, Workspace, KnowledgeCheck, ReviseMistakes, Profile
│   │   ├── App.jsx & main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── docs/
    ├── architecture.md                 # System architecture & answer locking protocol
    ├── ai-architecture.md              # Gemini 3.7 Flash & prompt engineering specs
    └── api.md                          # Comprehensive REST API specifications
```

---

## 🚀 Quickstart & Setup

### 1. Environment Setup

Copy `.env.example` to `.env` in `backend/`:
```bash
cp backend/.env.example backend/.env
```

Set your configuration in `backend/.env`:
```ini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-3.7-flash
MONGODB_URI=
MONGODB_DB_NAME=codementor_db
JWT_SECRET=super_secret_codementor_jwt_key_2026_change_in_production
```

> **Note**: If `MONGODB_URI` is left blank, CodeMentor AI automatically initializes a high-performance in-memory async database store for rapid local development and testing.

### 2. Run the Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

FastAPI Interactive Docs will be accessible at: `http://localhost:8000/docs`

### 3. Run Backend Tests

```bash
cd backend
python -m pytest -v
```

### 4. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will open at: `http://localhost:5173`

---

## 🧪 Demo Scenarios Verification

### Scenario 1: New User Onboarding $\rightarrow$ Weakness Detection $\rightarrow$ Progressive Hints $\rightarrow$ Unlock
1. Register a new user (`Python`, `Intermediate`).
2. Complete the **Knowledge Check** (Score high in Loops/Arrays, fail Recursion).
3. System automatically calculates `Calculated Level: Intermediate`, identifies `Weak Topics: ["recursion"]`, and generates an AI gap summary.
4. **Dashboard** recommends *"Factorial using Recursion"* explaining: *"Recommended because you struggled with recursion base cases"*.
5. Student opens the workspace and submits code without a base case:
   - **Attempt 1**: AI diagnoses `RUNTIME_ERROR` (`missing_base_case`), returns **Hint Level 1 (Socratic)**. Solution remains **LOCKED**.
   - **Attempt 2**: AI returns **Hint Level 2 (Conceptual)**. Solution remains **LOCKED**.
   - **Attempt 3**: Max attempts reached $\rightarrow$ Backend **UNLOCKS** solution with full step-by-step breakdown, optimal approach, and $O(n)$ time/$O(n)$ space complexity!
6. Profile records `missing_base_case` count and updates **Revise My Mistakes**.

### Scenario 2: Revise My Mistakes
1. Navigate to **Revise Mistakes**.
2. Shows prioritized recurring errors with specific tutor advice and matched corrective exercises.

### Scenario 3: Custom Problem ("Own Problem" Mode)
1. Navigate to **Custom Problem**.
2. Enter custom problem prompt and submit code for instant AI diagnosis, progressive hints, and multi-turn chat.

---

## 📜 Documentation Links
- [Architecture & Answer Locking Protocol](docs/architecture.md)
- [AI Architecture & Prompt Engineering](docs/ai-architecture.md)
- [REST API Reference](docs/api.md)
