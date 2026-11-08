# Safe AI Cup — StudyWiseAI Demo Script
### 3-Minute Presentation | Generative AI in Education

---

## Project Description (English)

**StudyWiseAI** is a fully offline, AI-powered learning platform that bridges the gap between a student's career ambitions and their daily study habits. Students enter a career goal — such as "I want to become a software engineer" — and StudyWiseAI instantly generates a personalised action plan: the subjects to study, skills to develop, activities to pursue, an education pathway, and short, medium, and long-term milestones. That plan connects directly to an integrated suite of tools — a Study Planner, Weekly Planner, Pomodoro timer, AI Chat assistant, NLP tools, and Progress tracker — all working together in one place.

Built with **FastAPI**, **React + TypeScript**, and **GPT4All (Orca Mini 3B)**, every feature runs entirely on the student's own device. No internet connection. No API keys. No subscription fees. All data is stored locally in SQLite, ensuring complete privacy. The AI is profession-aware, adapting its questions and plans based on the detected career field, with intelligent fallbacks that guarantee a fast, high-quality response every time.

StudyWiseAI makes personalised, career-driven education accessible to every student — not just those who can afford the cloud.

---

## وصف المشروع (عربي)

**StudyWiseAI** منصة تعليمية مدعومة بالذكاء الاصطناعي تعمل بالكامل دون اتصال بالإنترنت، وتهدف إلى سد الفجوة بين طموحات الطالب المهنية وعاداته الدراسية اليومية. يُدخل الطالب هدفه المهني — مثل "أريد أن أصبح مهندس برمجيات" — ليقوم StudyWiseAI فوراً بتوليد خطة عمل مخصصة تشمل: المواد الدراسية، والمهارات الواجب تطويرها، والأنشطة الموصى بها، ومسار التعليم المناسب، إضافةً إلى أهداف قصيرة ومتوسطة وطويلة المدى. وتتكامل هذه الخطة مباشرةً مع مجموعة متكاملة من الأدوات تشمل: مخطط الدراسة، والمخطط الأسبوعي، وموقت بومودورو، ومساعد الدردشة بالذكاء الاصطناعي، وأدوات معالجة اللغة الطبيعية، ومتتبع التقدم — كل ذلك في مكان واحد.

تم تطوير المنصة باستخدام **FastAPI** و**React + TypeScript** و**GPT4All (Orca Mini 3B)**، وتعمل جميع ميزاتها على جهاز الطالب مباشرةً دون الحاجة إلى اتصال بالإنترنت أو مفاتيح API أو رسوم اشتراك. تُخزَّن جميع البيانات محلياً في قاعدة بيانات SQLite لضمان الخصوصية التامة. يتمتع الذكاء الاصطناعي بوعي مهني متكيف، إذ يُعدّل أسئلته وخططه بناءً على المجال الوظيفي المُكتشف، مع آليات احتياطية ذكية تضمن استجابةً سريعة وعالية الجودة في كل مرة.

يجعل **StudyWiseAI** التعليم الشخصي القائم على المسار المهني في متناول كل طالب — وليس فقط من يستطيع تحمّل تكاليف الخدمات السحابية.

---

---

## ⏱ 0:00 – 0:30 | SEGMENT 1: Introduction & Problem Statement (30s)

**[On screen: Team name, school name, StudyWiseAI logo]**

> "Every day, millions of students sit down to study — and have no idea where to start.
>
> They don't know which subjects to prioritise. They don't know how to get from where they are today to the career they want tomorrow. And the tools that exist? Either too generic, too expensive, or not private enough to trust.
>
> We are **[Team Name]** from **[School Name]**, and we built **StudyWiseAI** — a fully offline, AI-powered learning platform that turns a career goal into a complete, personalised study roadmap.
>
> The pain point we're solving: **students lack a connected system** that links their career ambitions to daily study habits — without relying on the cloud, subscriptions, or compromising their data."

---

## ⏱ 0:30 – 1:30 | SEGMENT 2: Working Model Demonstration (60s)

**[Switch to live app — screen share or device recording]**

> "Let me show you how it works — live, right now."

**[Step 1 — Input: 0:30–0:40]**
> "A student logs in and navigates to Career Counseling. They type: *'I want to become a software engineer.'*"

**[Step 2 — AI Processing: 0:40–0:55]**
> "StudyWiseAI generates three tailored onboarding questions — asking about their current technical background, their motivation, and their target timeline. The AI adapts these questions based on the profession detected. A medical student gets different questions than an engineering student."

**[Step 3 — Output: 0:55–1:15]**
> "The student answers, and the AI produces a **full career action plan** — specific subjects to study, activities like internships and clubs, a skill development roadmap, an education pathway, and short, medium, and long-term milestones."

**[Step 4 — Integration: 1:15–1:30]**
> "One click on *'Add to Study Planner'* saves this entire plan. It immediately appears as a structured study plan card — ready to drive the Weekly Planner and Pomodoro timer. The student's career goal is now connected directly to their daily schedule."

---

## ⏱ 1:30 – 2:15 | SEGMENT 3: Technical Depth & Innovation (45s)

**[On screen — 3 visual slides:]**
1. **The innovation gap** — a simple side-by-side comparison slide: *Existing tools* (ChatGPT, Google, generic planners) on the left — isolated, generic, cloud-dependent, costly. *StudyWiseAI* on the right — connected, personalised, offline, free.
2. **The career-to-curriculum pipeline** — a visual flowchart: `Career Goal → AI Profiling Questions → Personalised Action Plan → Study Planner → Pomodoro Sessions → Progress Tracking`. One arrow, one connected journey. No other tool does this end-to-end.
3. **Offline-first innovation** — a striking visual: a WiFi icon with a cross through it, next to the StudyWiseAI logo and the text *"Full AI. Zero Internet."* Reinforce that running a 3-billion-parameter model locally — for free, forever — is the core innovation.

> "What makes us innovative? Three things: one connected pipeline — career goal, to plan, to daily habit. Full AI running offline, completely free, no internet needed. And a profession-aware model that gives a doctor different guidance than an engineer. Nothing else does all three."

---

## ⏱ 2:15 – 2:45 | SEGMENT 4: Sustainability & Ethics (30s)

**[On screen: privacy/ethics visual — e.g. lock icon, no-cloud icon]**

> "We took responsible design seriously from day one."
>
> "**Data privacy**: all user data — study plans, progress, chat history — is stored in a local SQLite database on the device. Nothing leaves the machine. No third-party servers, no data harvesting."
>
> "**Preventing over-reliance**: StudyWiseAI is built as a *guide*, not a crutch. The AI provides a framework, but students make decisions — what to study, how to adapt, what goals to set. The Pomodoro timer and progress tracker reinforce active effort, not passive consumption."
>
> "**Preventing bias**: we use structured, profession-specific templates as fallbacks when the AI output is empty or low-quality, ensuring every student receives a fair, complete response regardless of model performance."
>
> "**No plagiarism vector**: the AI generates plans and guidance — not essays or assessments to submit. Critical thinking stays with the student."

---

## ⏱ 2:45 – 3:00 | SEGMENT 5: Conclusion & Call to Action (15s)

**[On screen: StudyWiseAI logo + tagline]**

> "StudyWiseAI is a **working model** — running locally, end-to-end, right now.
>
> It connects a student's career ambition to their daily study habits, privately, for free, on any laptop.
>
> We believe every student deserves a personalised AI tutor — not just the ones who can afford the cloud.
>
> **StudyWiseAI. Study smarter. Start today.**"

---

## Presenter Notes

| Time | Key Action | What's on Screen |
|------|-----------|-----------------|
| 0:00 | Speaker 1 introduces problem | Team slide / problem graphic |
| 0:30 | Speaker 2 takes over for demo | Live app — Career Counseling |
| 0:40 | Type profession into app | AI question output |
| 0:55 | Scroll through action plan | Generated career plan |
| 1:15 | Click "Add to Study Planner" | Study Plans tab |
| 1:30 | Speaker 1 returns for tech section | Architecture / code |
| 2:15 | Speaker 2 covers ethics | Privacy/ethics visual |
| 2:45 | Both speakers for close | Logo + tagline |

### Tips
- Practice the demo flow at least 5 times before the presentation.
- Have the app already logged in and on the Career Counseling tab before you begin.
- If the local AI model is slow, the template fallback will respond instantly — mention this briefly as a feature ("our system has intelligent fallbacks to guarantee a fast response").
- Keep energy high on the demo segment — it's the most important 60 seconds.
