# StudyWiseAI

An AI-powered learning platform that provides personalised career-driven study plans, a local AI assistant, Pomodoro sessions, progress tracking, NLP tools, and a weekly planner — all running fully offline with no external AI API required.

---

## Features

### 🎓 Career Counseling
- Enter any career goal (e.g. "I want to become a doctor") and receive a profession-aware action plan
- AI asks tailored onboarding questions based on your profession (medical, engineering, legal, technology, or general)
- Generates a structured plan covering subjects, skills, short/medium/long-term milestones, and next steps
- One-click **Add to Study Planner** instantly saves the plan without a second AI call

### 📚 Study Plans
- All saved career plans are visible in the **Study** tab under "My Study Plans"
- Each card shows subject, difficulty, estimated hours, and creation date
- **View full plan** opens a detail modal with:
  - Subjects to study
  - Skills to develop
  - Recommended resources
  - Milestones (short / medium / long-term)
  - Weekly learning task table with priorities
  - Suggested daily activities
- Delete individual plans at any time

### ⚡ Pomodoro Timer
- Customisable session durations (25, 30, 45, 60+ minutes)
- Set a goal for each session before starting
- Completed sessions are automatically saved to your progress history

### 📅 Weekly Study Planner
- Visual 7-day calendar with colour-coded study events
- Add, edit, and remove sessions for any subject
- Shows total planned hours per week

### 💬 AI Study Assistant
- Chat interface powered by the local **orca-mini-3b** model (GPT4All)
- Ask questions on any subject and receive instant explanations
- Conversation history preserved within each session

### 🤖 NLP Tools
- **Text Summarisation** — condense long notes into key points
- **Sentiment Analysis** — detect tone and emotional context
- **Grammar Check** — identify and improve writing quality
- **Paraphrasing** — rephrase content for better understanding

### 📈 Progress Tracking
- Dashboard showing total study time, session count, and daily streaks
- Per-session history with subject, duration, and timestamp
- Achievement milestones as sessions accumulate

### 🔐 Authentication
- JWT-based registration and login
- All data is scoped to the authenticated user
- Persistent sessions via token storage

---

## Technology Stack

### Backend
| Component | Technology |
|---|---|
| Framework | FastAPI 0.115.0 |
| Language | Python 3.11+ |
| Database | SQLite (SQLAlchemy ORM) |
| Authentication | JWT (python-jose + bcrypt) |
| AI Model | GPT4All — orca-mini-3b-gguf2-q4_0 (local, offline) |
| AI Threading | `threading.Lock()` for safe single-threaded model access |
| Cache | Redis (optional — app runs without it) |

> **Pinned dependencies** — `pydantic==2.9.0`, `annotated-types==0.7.0`, and `pydantic-core==2.23.2` must stay at these versions. pip may auto-upgrade pydantic to 2.12+ which breaks the `annotated_types` import.

### Frontend
| Component | Technology |
|---|---|
| Framework | React 18 + TypeScript |
| Bundler | Vite |
| Styling | Tailwind CSS |
| State | React Context (Auth, Theme) |
| HTTP | Axios (via `apiService`) |

---

## Getting Started

### Prerequisites
- Python 3.11 or 3.12 (3.13 has C-extension issues with some packages)
- Node.js 18+
- Git

### 1 — Backend

```bash
# Clone and enter the project
git clone <repo-url>
cd StudyWiseAI

# Create and activate virtual environment
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

# Install dependencies (exact versions are important)
pip install -r requirements.txt

# Initialise the database
python -c "from app.core.init_db import init_db; init_db()"

# Start the API server
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

### 2 — Download the AI Model

```bash
python download_orca_mini.py
```

This downloads `orca-mini-3b-gguf2-q4_0.gguf` (~2 GB) into the GPT4All models directory. The server runs without it but AI features will fall back to template responses.

### 3 — Frontend

```bash
cd frontend-react
npm install
npm run dev
```

The React app will be available at `http://localhost:5173`.

---

## Project Structure

```
StudyWiseAI/
├── app/
│   ├── api/
│   │   ├── ai_assistant.py     # Career counseling, NLP, chat endpoints
│   │   ├── auth.py             # Register / login
│   │   ├── progress.py         # Study session tracking
│   │   ├── reminders.py        # Reminder endpoints
│   │   └── study_plans.py      # CRUD for study plans
│   ├── core/
│   │   ├── auth.py             # JWT helpers, get_current_user
│   │   ├── config.py           # Settings (env vars)
│   │   ├── database.py         # SQLAlchemy engine + session
│   │   └── init_db.py          # Table creation on startup
│   ├── models/
│   │   └── database.py         # ORM models (User, StudyPlan, etc.)
│   ├── services/
│   │   └── ai_service.py       # GPT4All wrapper, profession templates
│   └── main.py                 # FastAPI app, router registration
├── frontend-react/
│   └── src/
│       ├── components/
│       │   ├── ai/             # NLPModal
│       │   ├── auth/           # LoginForm, RegisterForm
│       │   ├── career/         # CareerCounselingModal
│       │   ├── chat/           # ChatModal
│       │   ├── common/         # Navigation, HomePage, Hero, etc.
│       │   ├── dashboard/      # ProgressModal
│       │   └── study/          # PomodoroModal, WeeklyPlannerModal,
│       │                       # StudyPlanDetailModal
│       ├── context/            # AuthContext, ThemeContext
│       ├── services/           # api.ts — typed Axios wrapper
│       └── types/              # TypeScript interfaces
├── tests/                      # pytest test files
├── requirements.txt            # Pinned Python dependencies
└── requirements-minimal.txt   # Minimal install for constrained environments
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./studywise.db
REDIS_URL=redis://localhost:6379   # optional
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Known Constraints

| Issue | Detail |
|---|---|
| Pydantic version | Must be pinned to `2.9.0` — higher versions rename internal symbols used by FastAPI 0.115 |
| AI model thread safety | `orca-mini-3b` is not thread-safe; a `threading.Lock()` serialises all inference calls |
| AI response quality | The local model occasionally returns empty responses; the service automatically falls back to structured templates |
| Python 3.13 | `pandas` and `numpy` wheels are unavailable without a C compiler; use Python 3.11/3.12 |