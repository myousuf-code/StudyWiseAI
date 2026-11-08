# STOGO FEST — StudyWiseAI Presentation Script
**Theme:** Reboot: The Rhythm of Life
**Duration:** 3 Minutes (~420 spoken words @ ~140 wpm)
**Participants:** Person A | Person B
**Format:** Intro → Code Recording → Website Demo (20s) → Conclusion

---

## WORD COUNT BALANCE

| Participant | Approx. Words | Approx. Time |
|-------------|--------------|--|
| Person A    | ~210 words   | ~90 seconds  |
| Person B    | ~210 words   | ~90 seconds  |

## SEGMENT TIMING

| Segment | Duration | Time |
|---------|----------|------|
| 1 — Introduction | 50 seconds | 0:00 – 0:50 |
| 2 — Code Recording | 65 seconds | 0:50 – 1:55 |
| 3 — Website Demo | **20 seconds** | 1:55 – 2:15 |
| 4 — Conclusion | 45 seconds | 2:15 – 3:00 |

---

## FULL SCRIPT

---

### SEGMENT 1 — INTRODUCTION [0:00 – 0:50]
*Camera on both presenters*

**PERSON A:**
> "Hi, I'm [Name], and this is [Name]. Today we're presenting **StudyWiseAI** — a fully offline, AI-powered learning platform designed to help students plan smarter, stay focused, and reach their career goals. Our project directly connects to this year's theme, **Reboot: The Rhythm of Life**. In a world where students are overwhelmed and burned out, StudyWiseAI gives them the tools to reset, rebuild healthy study habits, and find their sustainable rhythm — both academically and professionally."

**PERSON B:**
> "StudyWiseAI is unique because it runs entirely on your own device — no internet, no paid API subscriptions, and no privacy concerns. Everything is built from scratch using a **FastAPI Python backend** with JWT authentication, an SQLite database, and a **React TypeScript frontend**. At its core, an offline **GPT4All AI model** powers intelligent, personalised guidance — all completely free. Let's quickly look at how it's built."

---

### SEGMENT 2 — CODE RECORDING [0:50 – 1:55]
*Screen: VS Code — switch between backend and frontend files*

**PERSON A** *(show app/services/ai_service.py + app/core/auth.py)*:
> "Here's the heart of the app — our AI service. We're using **GPT4All's Orca Mini 3B model**, which runs completely offline on your machine. We've implemented thread-safe locking so the model handles requests without crashing under load. The backend is built on FastAPI — here you can see our authentication module, which uses **bcrypt** for password hashing and **python-jose** for JWT token generation. Every API endpoint is protected, with tokens validated on every request."

**PERSON B** *(show frontend-react/src/components/ folder + services/api.ts)*:
> "On the frontend, every feature is a self-contained React component — here's the **Career Counseling modal**, the **AI Chat interface**, the **NLP Tools panel**, and the **Pomodoro Timer**. All components share a centralised **Axios API service layer**, which handles authentication headers and error responses in one place. Routing is entirely state-driven with tabs — making the app feel fast with no page reloads. The full codebase is strictly typed with **TypeScript**."

---

### SEGMENT 3 — WEBSITE DEMO [1:55 – 2:15] *(20 seconds)*
*Screen: Live browser — rapid feature flythrough*

**PERSON A** *(Login → Career Counseling → Study Plans)*:
> "Here's the live site — secure login, AI generates a full career action plan, saved to your study planner instantly."

**PERSON B** *(scroll through remaining features)*:
> "Plus Pomodoro Timer, Weekly Planner, Progress Dashboard, AI Chat, and NLP Tools — all one click away."

---

### SEGMENT 4 — CONCLUSION [2:15 – 3:00]
*Camera back on both presenters*

**PERSON A:**
> "StudyWiseAI isn't just a tool — it's a **personal learning companion**. It helps students reboot their approach to studying and build a rhythm that is sustainable, personalised, and career-driven. From generating AI career plans to tracking daily progress, every feature contributes to the **wellbeing and growth** of the student — physically through focus sessions, mentally through structured planning, and professionally through career guidance."

**PERSON B:**
> "Whether it's planning a career at 2pm, running a Pomodoro session at 8pm, or getting AI help at midnight — StudyWiseAI is available **fully offline, always**. It supports the whole student journey, rebalancing how young people learn in the digital age. We believe this is how the rhythm of life should be — intentional, supported, and smart. **Thank you!**"

---

## SCREEN RECORDING ORDER

| Time        | Person   | Screen to Show                                              |
|-------------|----------|-------------------------------------------------------------|
| 0:00–0:50   | Both     | Camera on presenters                                        |
| 0:50–1:22   | Person A | app/services/ai_service.py → app/core/auth.py               |
| 1:22–1:55   | Person B | frontend-react/src/components/ → frontend-react/src/services/api.ts |
| 1:55–2:05   | Person A | Browser: Login page → Career Counseling → Study Plans       |
| 2:05–2:15   | Person B | Browser: Pomodoro → Planner → Progress → Chat → NLP (rapid) |
| 2:15–3:00   | Both     | Camera on presenters for conclusion                         |

---

## FILMING CHECKLIST (per competition guidelines)

- [ ] Mention project title, team names, and category/grade in the intro
- [ ] Clearly explain the "Reboot: The Rhythm of Life" theme connection
- [ ] Use supporting materials (slides/printouts) behind or beside the presenter
- [ ] Both members actively present with equal roles
- [ ] Keep final video under 3 minutes
- [ ] Record in a quiet, noise-free environment
- [ ] Camera covers both the working website and the presenters
- [ ] Maintain eye contact with the camera
- [ ] End with a proper conclusion summarising the project idea, impact, and theme
- [ ] Upload to Google Drive and set access to "Anyone with the link can view"
