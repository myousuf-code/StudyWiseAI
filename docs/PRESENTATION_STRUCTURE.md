 # StudyWiseAI — Presentation Structure

---

## Slide 1 — Title Slide

**StudyWiseAI**
*Your Offline, AI-Powered Personal Learning Companion*

- Team Name: [Team Name]
- School / Institution: [School Name]
- Date: [Presentation Date]

---

## Slide 2 — Problem Statement

### What problem are we solving?

Students across the world face three connected challenges:

1. **No clear direction** — Most students don't know which subjects to prioritise or how their daily study habits connect to their long-term career goals.
2. **Disconnected tools** — Existing apps (Google, ChatGPT, generic planners) are isolated. A student must jump between multiple platforms just to plan, study, and track progress — with no single thread connecting it all.
3. **Affordability and privacy** — AI-powered tutoring tools are either expensive (subscription fees) or cloud-dependent, raising serious data privacy concerns for students.

### Who is affected?

- Students at every level — secondary school, university, and self-learners
- Students in areas with limited or unreliable internet access
- Students who cannot afford paid AI platforms

### Why does it matter?

> *"Every day, millions of students sit down to study — and have no idea where to start."*

Without a personalised roadmap, students waste hours on low-priority content, lose motivation, and fall short of their potential. The gap between a career ambition and daily study habits remains unaddressed.

---

## Slide 3 — Proposed Solution

### What is StudyWiseAI?

**StudyWiseAI** is a fully offline, AI-powered learning platform that turns a student's career goal into a complete, personalised study roadmap — and connects that roadmap directly to their daily study tools.

### How does it solve the problem?

1. A student enters a career goal: *"I want to become a software engineer."*
2. The AI asks three profession-tailored onboarding questions (background, motivation, timeline).
3. A full **Career Action Plan** is generated — covering subjects, skills, activities, education pathway, and short / medium / long-term milestones.
4. One click on **"Add to Study Planner"** saves the plan and connects it to the student's Weekly Planner, Pomodoro timer, and Progress tracker.
5. Every tool works together in one place — no switching apps, no internet required.

### What makes it unique?

| Feature | Competitors (ChatGPT, Google, etc.) | StudyWiseAI |
|---|---|---|
| Offline capability | ❌ Cloud-dependent | ✅ Fully offline |
| Career-to-curriculum pipeline | ❌ Isolated responses | ✅ End-to-end connected journey |
| Profession-aware AI | ❌ Generic | ✅ Adapts to medical, engineering, law, tech, and more |
| Cost | ❌ Subscription fees | ✅ Completely free |
| Data privacy | ❌ Data sent to external servers | ✅ All data stays on your device |
| Integrated study tools | ❌ Separate apps needed | ✅ Planner, Pomodoro, Progress — all in one |

---

## Slide 4 — Technology & Approach

### Architecture Overview

```
Career Goal → AI Profiling Questions → Personalised Action Plan
      ↓
Study Planner → Weekly Planner → Pomodoro Timer → Progress Tracker
```

One connected pipeline. No other tool does this end-to-end.

### Backend

| Component | Technology | Purpose |
|---|---|---|
| Framework | **FastAPI** (Python) | High-performance REST API |
| Database | **SQLite** + SQLAlchemy ORM | Local, private data storage |
| Authentication | **JWT** (python-jose + bcrypt) | Secure, token-based login |
| AI Model | **GPT4All — Orca Mini 3B** (GGUF) | Offline large language model |
| Thread Safety | `threading.Lock()` | Safe single-threaded model access |
| Fallback System | Profession-specific templates | Guarantees fast, quality responses |

### Frontend

| Component | Technology | Purpose |
|---|---|---|
| Framework | **React 18 + TypeScript** | Type-safe, component-based UI |
| Bundler | **Vite** | Fast build and hot-reload |
| Styling | **Tailwind CSS** | Responsive, utility-first design |
| API Layer | **Axios** (centralised service) | Unified auth headers + error handling |
| Routing | State-driven tabs | Instant navigation, no page reloads |

### Key Technical Innovations

1. **Offline-first AI** — A 3-billion-parameter language model runs entirely on the student's laptop. No Wi-Fi, no API keys, no costs — ever.
2. **Profession-aware prompting** — The AI detects the career field (medical, engineering, legal, technology, general) and tailors both its questions and the generated plan accordingly.
3. **Intelligent fallback system** — Structured templates guarantee a complete, high-quality response even when the model output is slow or incomplete.
4. **Thread-safe model access** — `threading.Lock()` prevents crashes under concurrent requests, making the app robust for real use.

---

## Slide 5 — Prototype

### Live Features (working model)

| Feature | What It Does |
|---|---|
| **Career Counseling** | Enter any career goal → AI generates personalised action plan with subjects, skills, milestones, and activities |
| **Study Plans** | Career plans saved as structured cards with full detail view (resources, milestones, weekly task table) |
| **Weekly Planner** | 7-day visual calendar — add, edit, remove study sessions with colour-coded subjects |
| **Pomodoro Timer** | Customisable sessions (25–60+ min), set a focus goal, auto-saves to progress history |
| **AI Chat Assistant** | Ask any academic question — answered by the local Orca Mini 3B model, offline |
| **NLP Tools** | Text summarisation, sentiment analysis, grammar check, and paraphrasing |
| **Progress Tracker** | Dashboard: total study time, session count, streaks, per-subject history |
| **Authentication** | JWT-based register/login — all data scoped to the authenticated user |

### Screenshots / Demo Flow

1. **Login screen** → secure authentication
2. **Career Counseling** → type "I want to become a doctor" → AI questions → full action plan generated
3. **"Add to Study Planner"** → one click saves to Study Plans tab
4. **Study Plan detail modal** → subjects, skills, resources, milestones, weekly table
5. **Weekly Planner** → colour-coded 7-day schedule
6. **Pomodoro Timer** → set goal, start session, auto-logged
7. **Progress Dashboard** → study time, streaks, session history
8. **AI Chat** → ask a question, get an instant offline answer
9. **NLP Tools** → paste text → summarise / check grammar / paraphrase

> **Demo Tip:** Have the app already running and logged in before the presentation. Navigate: Career Counseling → Study Plans → Pomodoro → Planner → Progress → Chat → NLP.

---

## Slide 6 — Impact & Benefits

### Positive Impact

**For Students:**
- Eliminates the "I don't know where to start" problem — every student gets a personalised roadmap within seconds
- Connects long-term career ambitions to daily study habits for the first time in a single app
- Reduces study-related anxiety through structured planning and focused Pomodoro sessions
- Available 24/7, fully offline — on any laptop, anywhere, any time

**For Accessibility:**
- Completely free — no subscriptions, no API costs
- Works without internet — reaches students in low-connectivity areas
- Runs on a standard consumer laptop — no specialised hardware required

**For Privacy & Ethics:**
- All data (plans, chats, progress) stored locally in SQLite — nothing sent to external servers
- AI is a *guide*, not a replacement for student effort — critical thinking stays with the student
- Profession-specific fallback templates ensure fairness regardless of model performance
- No essay-generation or academic dishonesty vectors — the AI generates plans and guidance only

**Broader Impact:**
- Democratises personalised AI tutoring — not just for students who can afford cloud services
- Could reduce dropout rates by giving students clearer direction and daily accountability
- Applicable in schools, universities, and self-learning contexts worldwide

---

## Slide 7 — Team & Roles

| Team Member | Role | Responsibilities |
|---|---|---|
| [Name 1] | **Project Lead / Backend Developer** | FastAPI architecture, authentication system (JWT + bcrypt), database schema (SQLAlchemy + SQLite), AI model integration (GPT4All), thread safety |
| [Name 2] | **Frontend Developer / UI Designer** | React + TypeScript components, Tailwind CSS styling, Axios API service layer, state management, responsive design |
| [Name 3] | **AI / NLP Engineer** | Orca Mini 3B model integration, profession-aware prompt engineering, fallback template system, NLP tools (summarisation, sentiment, grammar, paraphrasing) |
| [Name 4] | **QA / Testing & Documentation** | Test suite (pytest), feature documentation, demo preparation, presentation scripting |

> *Replace names and adjust roles to match your actual team composition.*

---

## Presentation Tips

- **Practice the demo at least 5 times** — live demos are the strongest part of your pitch
- Pre-load the app and log in **before** the judging session begins
- If the AI model is slow, the fallback template responds instantly — mention it as a *feature*: *"Our system has intelligent fallbacks to guarantee a fast response every time"*
- Each team member should own and confidently explain their specific section
- Judges may ask: *"Why offline?"* → Answer: privacy, accessibility, zero cost, works anywhere
- Judges may ask: *"How is this different from ChatGPT?"* → Answer: see the comparison table on Slide 3
