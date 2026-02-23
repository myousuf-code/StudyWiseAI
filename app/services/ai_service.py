"""
AI Assistant Service
Local GPT4All integration for study assistance and chat
"""
from gpt4all import GPT4All
from typing import List, Dict, Optional
from app.core.config import settings
from app.models.database import User, StudyPlan, ProgressRecord
import asyncio
import functools
import threading

class AIAssistantService:
    """Service class for local AI-powered study assistance using GPT4All"""
    
    def __init__(self):
        # Use orca-mini model (more stable than Phi-3)
        # Orca-mini: Smaller, more stable with good quality
        self.model_name = "orca-mini-3b-gguf2-q4_0.gguf"
        self.fallback_model_name = "Phi-3-mini-4k-instruct.Q4_0.gguf"  # Fallback if primary fails
        self._model = None
        self._model_name_in_use = self.model_name
        self._last_request_time = None
        self._model_lock = threading.Lock()  # Prevent concurrent model access (causes access violations)
        
    def _cleanup_model(self):
        """Properly close and cleanup the model"""
        if self._model is not None:
            try:
                self._model.close()
            except:
                pass
        self._model = None
        
    def _get_model(self):
        """Lazy load the model to avoid loading it on import"""
        if self._model is None:
            try:
                print(f"Loading local AI model: {self._model_name_in_use}...")
                self._model = GPT4All(self._model_name_in_use)
                print(f"✅ Model loaded successfully: {self._model_name_in_use}")
            except Exception as e:
                print(f"⚠️ Failed to load {self._model_name_in_use}: {e}")
                
                # Try fallback model
                if self._model_name_in_use != self.fallback_model_name:
                    print(f"Trying fallback model: {self.fallback_model_name}...")
                    try:
                        self._model_name_in_use = self.fallback_model_name
                        self._model = GPT4All(self.fallback_model_name)
                        print(f"✅ Fallback model loaded: {self.fallback_model_name}")
                    except Exception as e2:
                        print(f"❌ Fallback model also failed: {e2}")
                        raise Exception(f"Both models failed to load. Primary: {e}, Fallback: {e2}")
                else:
                    raise Exception(f"Failed to load model: {e}")
        return self._model
        
    async def _generate_response(self, prompt: str, system_prompt: str = None) -> Dict:
        """Generate response using local GPT4All model"""
        try:
            # Use orca-mini instruction format: ### System / ### User / ### Response
            # Without this format the model outputs nothing (0 chars)
            if system_prompt:
                full_prompt = f"### System:\n{system_prompt}\n\n### User:\n{prompt}\n\n### Response:\n"
            else:
                full_prompt = f"### User:\n{prompt}\n\n### Response:\n"
                
            # Run model generation in thread pool to avoid blocking
            # Lock ensures only one generation runs at a time - concurrent access causes access violations
            loop = asyncio.get_event_loop()
            
            def generate():
                with self._model_lock:
                    try:
                        model = self._get_model()
                        response = model.generate(
                            full_prompt,
                            max_tokens=600,
                            temp=0.3,
                            top_p=0.7
                        )
                        return response
                    except Exception as generation_error:
                        error_str = str(generation_error)
                        print(f"[AI] Generation error: {error_str}")
                        # On memory/access violation, clean up model so next call reloads it fresh
                        if "access violation" in error_str.lower() or "segmentation" in error_str.lower():
                            print("[AI] Detected memory error, cleaning up model for next request...")
                            self._cleanup_model()
                        raise
            
            response = await loop.run_in_executor(None, generate)
            
            return {
                "success": True,
                "response": response.strip(),
                "usage": "local"
            }
                
        except Exception as e:
            print(f"[AI] Response generation failed: {str(e)}")
            return {
                "success": False,
                "error": f"Local AI error: {str(e)}"
            }
        
    async def generate_study_plan(
        self, 
        user: User, 
        subject: str, 
        duration_weeks: int,
        difficulty_level: str,
        learning_style: str
    ) -> Dict:
        """Generate AI-powered personalized study plan"""
        
        system_prompt = "You are an expert educational consultant who creates personalized study plans. Always respond with helpful, structured study advice."
        
        user_prompt = f"""
        Create a personalized study plan for a {difficulty_level} level student studying {subject}.
        
        Student Profile:
        - Learning Style: {learning_style}
        - Available Time: {duration_weeks} weeks
        - Current Goals: {user.study_goals or 'General improvement'}
        
        Please provide a structured study plan with:
        1. Weekly breakdown of topics (Week 1, Week 2, etc.)
        2. Recommended study materials and resources
        3. Key milestones and assessments
        4. Daily time allocation suggestions
        5. Learning objectives for each week
        
        Keep the response practical and achievable for a student.
        """
        
        return await self._generate_response(user_prompt, system_prompt)
    
    async def get_study_help(
        self, 
        user: User,
        question: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Get AI assistance for study questions"""
        
        system_prompt = "You are a helpful AI tutor who provides clear, encouraging study assistance. Give practical, educational answers that help students learn effectively."
        
        # Build context from user's study history
        context_info = ""
        if context and context.get("current_topic"):
            context_info = f"Currently studying: {context['current_topic']}\n"
        if user and user.learning_style:
            context_info += f"Learning style: {user.learning_style}\n"
            
        user_prompt = f"""
        {context_info}
        Student Question: {question}
        
        Please provide a helpful, educational response that:
        1. Answers the question clearly and simply
        2. Provides relevant examples when helpful
        3. Suggests follow-up study activities if appropriate
        4. Encourages the student's learning journey
        
        Keep your response concise but thorough.
        """
        
        return await self._generate_response(user_prompt, system_prompt)
    
    async def analyze_progress(
        self, 
        user: User, 
        progress_records: List[ProgressRecord]
    ) -> Dict:
        """Analyze user progress and provide insights"""
        
        if not progress_records:
            return {"success": True, "insights": "No progress data available yet. Start studying to see insights!"}
        
        # Create summary of progress
        total_time = sum(record.time_spent for record in progress_records)
        avg_accuracy = sum(record.accuracy_score or 0 for record in progress_records if record.accuracy_score) / len([r for r in progress_records if r.accuracy_score]) if any(r.accuracy_score for r in progress_records) else 0
        subjects = list(set(record.subject for record in progress_records))
        
        system_prompt = "You are an educational data analyst who provides encouraging, actionable insights to help students improve their learning."
        
        user_prompt = f"""
        Analyze this student's learning progress and provide insights:
        
        Study Summary:
        - Total study time: {total_time} minutes
        - Average accuracy: {avg_accuracy:.1f}%
        - Subjects studied: {', '.join(subjects)}
        - Learning sessions: {len(progress_records)}
        - Learning style: {user.learning_style if user else 'Not specified'}
        
        Please provide:
        1. Key strengths observed in their study pattern
        2. Areas for improvement
        3. Personalized recommendations for better learning
        4. Motivational encouragement
        
        Keep the response positive and actionable.
        """
        
        return await self._generate_response(user_prompt, system_prompt)
    
    async def generate_quiz_questions(
        self, 
        topic: str, 
        difficulty: str, 
        question_count: int = 5
    ) -> Dict:
        """Generate quiz questions for a topic"""
        
        system_prompt = "You are an educational content creator who makes engaging, fair quiz questions that test understanding rather than just memorization."
        
        user_prompt = f"""
        Generate {question_count} {difficulty} level quiz questions about {topic}.
        
        Format each question exactly like this:
        
        Question 1: [question text]
        A) option1
        B) option2  
        C) option3
        D) option4
        Answer: [correct option letter]
        Explanation: [brief explanation of why this is correct]
        
        Question 2: [question text]
        A) option1
        B) option2
        C) option3  
        D) option4
        Answer: [correct option letter]
        Explanation: [brief explanation of why this is correct]
        
        Continue this format for all {question_count} questions. Make questions that test understanding and application, not just memorization.
        """
        
        return await self._generate_response(user_prompt, system_prompt)

    async def start_career_counseling(
        self,
        user: User,
        target_profession: str
    ) -> Dict:
        """Start a career counseling session by asking initial questions"""

        # Try AI first with short timeout, fall back to template if slow
        try:
            system_prompt = "You are a career counselor. Ask 3 brief questions about their background, motivation, and timeline."

            user_prompt = f"Ask 3 questions for a student wanting to become a {target_profession}. Keep it brief."
            
            # Very short timeout for AI attempt
            ai_task = asyncio.create_task(self._generate_response(user_prompt, system_prompt))
            ai_response = await asyncio.wait_for(ai_task, timeout=30.0)
            
            # Check both success AND that response is not empty
            if ai_response.get("success") and ai_response.get("response", "").strip():
                print(f"[AI] Career counseling AI returned {len(ai_response.get('response', ''))} chars")
                return ai_response
            else:
                # Fall back to template if empty or failed
                empty_response = not ai_response.get("response", "").strip()
                if empty_response:
                    print(f"[AI] Career counseling AI returned empty response, using template for {target_profession}")
                return self._get_career_questions_template(target_profession)
                
        except asyncio.TimeoutError:
            print(f"[AI] Career counseling AI timeout, using template for {target_profession}")
            return self._get_career_questions_template(target_profession)
        except Exception as e:
            print(f"[AI] Career counseling error: {e}, using template")
            return self._get_career_questions_template(target_profession)

    def _get_career_questions_template(self, target_profession: str) -> Dict:
        """Fallback template for career counseling questions — profession-aware"""
        d = self._get_profession_plan_data(target_profession)
        prof_lower = target_profession.lower()

        # Tailor question 1 based on profession category
        if any(kw in prof_lower for kw in ["doctor","physician","surgeon","dentist","nurse","pharmacist","medical"]):
            q1 = "**Academic Background**: What is your current science GPA and have you completed prerequisite courses like Biology, Chemistry, or Physics?"
            q3 = "**Timeline & Entry Path**: Are you pursuing undergraduate pre-med, or are you already a graduate? Which country/system are you targeting (e.g., USMLE, PLAB)?"
        elif any(kw in prof_lower for kw in ["lawyer","attorney","solicitor","barrister","legal","law"]):
            q1 = "**Academic Background**: What is your current degree/GPA and have you taken any law or political science courses? Have you sat the LSAT or equivalent?"
            q3 = "**Timeline & Entry Path**: Are you targeting law school directly or considering a paralegal route first? Which jurisdiction are you aiming for?"
        elif any(kw in prof_lower for kw in ["engineer","engineering"]):
            q1 = "**Academic Background**: What is your current level of mathematics and physics? Have you done any engineering coursework or hands-on projects?"
            q3 = "**Timeline & Specialisation**: What engineering discipline interests you most (mechanical, electrical, civil, software, etc.) and what is your target timeline?"
        elif any(kw in prof_lower for kw in ["software","developer","programmer","data scientist","data analyst","machine learning","ai","cybersecurity","devops"]):
            q1 = "**Technical Background**: What programming languages or tools do you already know? Do you have any projects, courses, or work experience in tech?"
            q3 = "**Timeline & Specialisation**: What area of tech interests you most (web, data, AI, security, etc.) and how many hours per week can you commit to learning?"
        else:
            q1 = f"**Academic Background**: What is your current educational level and do you have any relevant coursework or experience related to {target_profession}?"
            q3 = f"**Timeline & Commitment**: What is your target timeline for entering this field as a {target_profession}, and how much time can you dedicate to preparation each week?"

        questions = f"""Great! You want to pursue a career as a {target_profession}. Let me ask you a few questions to better understand your background and goals:

1. {q1}

2. **Motivation & Interests**: What specifically draws you to becoming a {target_profession}? What aspects of this career excite you most, and are there any role models or experiences that inspired this choice?

3. {q3}

Please answer these questions in detail to help me create a personalised action plan for your career journey."""

        return {
            "success": True,
            "response": questions,
            "usage": "template_fallback"
        }

    async def generate_career_action_plan(
        self,
        user: User,
        target_profession: str,
        user_responses: str
    ) -> Dict:
        """Generate a comprehensive career action plan based on user responses"""

        try:
            system_prompt = "You are a career development expert who creates actionable, realistic career plans for students."

            user_prompt = f"""Create a career action plan for {target_profession}:

Student: {user_responses}

Include:
1. Key subjects (5-8 courses)
2. Activities (internships, clubs, projects)
3. Skills to develop
4. Education pathway
5. Milestones (6-12 months, 1-3 years, long-term)

Be specific and actionable."""

            # Try AI with timeout
            ai_task = asyncio.create_task(self._generate_response(user_prompt, system_prompt))
            ai_response = await asyncio.wait_for(ai_task, timeout=45.0)
            
            # Check both success AND that response is not empty
            if ai_response.get("success") and ai_response.get("response", "").strip():
                return ai_response
            else:
                # Fall back to template if empty or failed
                empty_response = not ai_response.get("response", "").strip()
                if empty_response:
                    print(f"[AI] Career plan AI returned empty response, using template for {target_profession}")
                else:
                    print(f"[AI] Career plan AI failed, using template for {target_profession}")
                return self._get_career_plan_template(target_profession)
                
        except asyncio.TimeoutError:
            print(f"[AI] Career plan generation timeout, using template for {target_profession}")
            return self._get_career_plan_template(target_profession)
        except Exception as e:
            print(f"[AI] Career plan error: {e}, using template")
            return self._get_career_plan_template(target_profession)
            
    # Profession-specific plan data keyed by keyword categories
    _PROFESSION_PLANS = {
        "medical": {
            "keywords": ["doctor", "physician", "surgeon", "dentist", "nurse", "pharmacist", "medical", "psychiatrist", "radiologist", "cardiologist", "pediatrician", "dermatologist", "anesthesiologist", "obstetrician"],
            "subjects": [
                "Biology & Human Anatomy",
                "Chemistry (Organic & Biochemistry)",
                "Physics & Biophysics",
                "Microbiology & Immunology",
                "Pharmacology",
                "Medical Ethics & Law",
                "Statistics & Research Methods",
                "Psychology & Patient Communication",
            ],
            "activities": """**Clinical & Practical Experience:**
- Hospital or clinic volunteering (minimum 100-200 hours)
- Medical/healthcare internships or shadowing programs
- Research assistant roles in medical labs

**Clubs & Organizations:**
- Pre-med or health professions club
- Red Cross or community health initiatives
- Medical journal reading groups

**Certifications & Exams:**
- CPR/First Aid certification
- MCAT preparation (for medical school)
- EMT certification for hands-on experience

**Networking:**
- Medical school open days and information sessions
- Connect with doctors/residents as mentors
- Attend healthcare conferences and seminars""",
            "skills": """**Clinical Skills:**
- Year 1-2: Core sciences (biology, chemistry, anatomy)
- Year 2-3: Clinical fundamentals and patient interaction
- Year 3-4: Rotations, diagnosis thinking, treatment planning

**Soft Skills:**
- Empathy and patient communication
- High-pressure decision-making
- Teamwork in multidisciplinary teams
- Attention to detail and precision""",
            "education": """- **Pre-med Bachelor's Degree**: Biology, Chemistry, or related (4 years)
- **Medical School (MBBS/MD)**: 4-6 years depending on country
- **Residency**: 3-7 years in specialty of choice
- **Fellowship** (optional): 1-3 years for sub-specialization
- **Licensing Exams**: USMLE (US), PLAB (UK), or local equivalent""",
            "short_term": [
                "Achieve strong GPA in science prerequisites",
                "Complete 100+ hours of healthcare volunteering",
                "Gain research or lab experience",
                "Start MCAT/medical entrance exam preparation",
                "Shadow a practising doctor in your target specialty",
            ],
            "medium_term": [
                "Secure medical school admission",
                "Develop clinical examination skills",
                "Complete core clinical rotations",
                "Build a strong medical school portfolio",
                "Pass licensing/boards Part 1",
            ],
            "long_term": [
                "Complete residency in chosen specialty",
                "Obtain full medical licence and board certification",
                "Establish independent clinical practice",
                "Pursue research and publish findings",
                "Consider fellowship for sub-specialization",
            ],
            "next_steps": [
                "Enrol in or strengthen prerequisite science courses this semester",
                "Arrange a hospital volunteering placement within 4 weeks",
                "Create a study schedule for MCAT/entrance exam preparation",
                "Reach out to 2-3 doctors for mentorship or shadowing",
                "Research medical school requirements and application timelines",
            ]
        },
        "engineering": {
            "keywords": ["engineer", "engineering", "mechanical", "electrical", "civil", "chemical", "aerospace", "biomedical", "structural", "environmental"],
            "subjects": [
                "Mathematics (Calculus, Linear Algebra, Differential Equations)",
                "Physics & Applied Mechanics",
                "Thermodynamics & Fluid Dynamics",
                "Materials Science",
                "Circuit Theory & Electronics",
                "Engineering Design & CAD",
                "Project Management",
                "Technical Report Writing",
            ],
            "activities": """**Practical Experience:**
- Engineering internships or co-op placements
- Design-build competitions (robotics, bridge, etc.)
- Industry-sponsored capstone projects

**Clubs & Organizations:**
- Engineering student society
- IEEE, ASME, or relevant professional body student chapter
- Hackathons and maker-faires

**Certifications:**
- AutoCAD / SolidWorks / MATLAB proficiency
- Engineering Intern (EIT) exam preparation
- Health & Safety certifications

**Networking:**
- Engineering career fairs and industry nights
- Professional engineers as mentors
- LinkedIn engineering communities""",
            "skills": """**Technical Skills:**
- Year 1-2: Engineering fundamentals and mathematics
- Year 2-3: Specialisation courses and CAD/simulation tools
- Year 3-4: Design projects, systems integration, and labs

**Soft Skills:**
- Analytical problem-solving
- Team collaboration in engineering projects
- Technical communication and report writing
- Time management across complex projects""",
            "education": """- **Bachelor's in Engineering**: 4-5 years (accredited program)
- **Professional Engineer (PE/CEng) Licence**: After 4 years work experience
- **Master's Degree** (optional): For research or advanced specialisation
- **Continuing Education**: Keep up with evolving standards and technologies""",
            "short_term": [
                "Excel in core maths and physics foundations",
                "Learn CAD software (AutoCAD, SolidWorks, or equivalent)",
                "Join an engineering student society or club",
                "Complete a personal or team design project",
                "Secure a summer internship at an engineering firm",
            ],
            "medium_term": [
                "Complete specialisation coursework and lab modules",
                "Obtain 2-3 industry internships",
                "Build a strong engineering portfolio",
                "Achieve relevant software/tool certifications",
                "Sit the Engineering Intern (EIT) exam",
            ],
            "long_term": [
                "Obtain Professional Engineer licence",
                "Lead engineering design projects",
                "Specialise in a high-demand area",
                "Pursue chartered status with a professional body",
                "Consider postgraduate research or management roles",
            ],
            "next_steps": [
                "Review and strengthen maths fundamentals this month",
                "Install and complete a CAD software tutorial within 6 weeks",
                "Attend next engineering career fair on campus",
                "Apply for summer engineering internships",
                "Identify your engineering specialisation and target courses",
            ]
        },
        "legal": {
            "keywords": ["lawyer", "attorney", "solicitor", "barrister", "judge", "legal", "law", "paralegal", "counsel"],
            "subjects": [
                "Constitutional & Administrative Law",
                "Contract Law & Tort",
                "Criminal Law & Procedure",
                "Corporate & Commercial Law",
                "Legal Research & Writing",
                "Evidence & Litigation",
                "Ethics & Professional Responsibility",
                "Negotiation & Dispute Resolution",
            ],
            "activities": """**Practical Experience:**
- Law firm internships or paralegal work
- Mock trial and moot court competitions
- Legal aid clinic volunteering

**Clubs & Organizations:**
- Law society or pre-law club
- Debate team
- Model United Nations

**Certifications & Exams:**
- LSAT preparation (for law school admission)
- Bar exam preparation materials
- Legal research tools (Westlaw, LexisNexis)

**Networking:**
- Attend bar association events
- Connect with practising lawyers as mentors
- Legal networking dinners and seminars""",
            "skills": """**Legal Skills:**
- Year 1-2: Legal research, writing, and foundational subjects
- Year 2-3: Specialisation and clinical/practical components
- Year 3+: Advocacy, negotiation, and client-facing skills

**Soft Skills:**
- Analytical reasoning and argumentation
- Persuasive written and oral communication
- Attention to detail under pressure
- Ethical judgment and professionalism""",
            "education": """- **Undergraduate Degree**: Law (LLB) or any degree + JD/LPC
- **Law School (JD/LLB/LLM)**: 3 years
- **Bar Exam / Solicitor Qualifying Exam (SQE)**: After graduation
- **Training Contract / Articles**: 2 years in a law firm
- **Continuing Legal Education (CLE)**: Ongoing requirement""",
            "short_term": [
                "Achieve strong academic GPA and LSAT/admissions score",
                "Gain paralegal or legal assistant experience",
                "Compete in at least one moot court competition",
                "Build legal research and writing skills",
                "Volunteer at a legal aid clinic",
            ],
            "medium_term": [
                "Secure law school admission",
                "Complete summer associate or clerkship programs",
                "Develop expertise in chosen practice area",
                "Win or place in a major moot court competition",
                "Build a professional legal network",
            ],
            "long_term": [
                "Pass the bar/SQE exam and obtain law licence",
                "Secure a training contract or associate position",
                "Develop a specialisation (corporate, criminal, family, etc.)",
                "Build client relationships and a reputation in your area",
                "Consider partnership track or independent practice",
            ],
            "next_steps": [
                "Begin LSAT/admissions exam preparation immediately",
                "Apply for law firm internship or paralegal role within 4 weeks",
                "Join a debate club or moot court team",
                "Read one legal case per week to build analytical intuition",
                "Research law school requirements and deadlines",
            ]
        },
        "technology": {
            "keywords": ["software", "developer", "programmer", "data scientist", "data analyst", "machine learning", "ai", "cybersecurity", "devops", "cloud", "web developer", "full stack", "frontend", "backend", "mobile developer", "ios", "android", "game developer", "systems"],
            "subjects": [
                "Data Structures & Algorithms",
                "Software Engineering & Design Patterns",
                "Databases & SQL",
                "Operating Systems & Networking",
                "Mathematics (Discrete Math, Statistics)",
                "Cloud Computing & DevOps",
                "Security Fundamentals",
                "Communication & Technical Writing",
            ],
            "activities": """**Practical Experience:**
- Software internships (2-3 during studies)
- Open source contributions on GitHub
- Freelance or contract projects

**Clubs & Organizations:**
- Coding clubs and hackathons
- Competitive programming (LeetCode, Codeforces)
- Tech startup incubators or university labs

**Projects & Certifications:**
- Build 5-10 portfolio projects addressing real problems
- AWS / Azure / GCP cloud certifications
- Relevant framework certifications (e.g., React, TensorFlow)

**Networking:**
- Attend tech meetups and conferences
- Contribute to developer communities (Stack Overflow, GitHub)
- LinkedIn tech community connections""",
            "skills": """**Technical Skills:**
- Year 1-2: Core programming languages and CS fundamentals
- Year 2-3: Frameworks, databases, and system design
- Year 3+: Cloud, security, specialisation

**Soft Skills:**
- Problem decomposition and debugging mindset
- Agile teamwork and code review culture
- Technical communication and documentation
- Continuous learning drive""",
            "education": """- **Bachelor's in Computer Science / Software Engineering**: 3-4 years
- **Alternative**: Coding bootcamps (3-6 months intensive)
- **Online Courses**: Coursera, Udemy, edX, Pluralsight
- **Certifications**: AWS, Google Cloud, Microsoft Azure
- **Graduate Degree** (optional): For research or leadership roles""",
            "short_term": [
                "Master at least one programming language deeply",
                "Complete 3 portfolio projects and publish on GitHub",
                "Solve 50+ algorithm problems on LeetCode",
                "Attend 2 hackathons",
                "Update resume and LinkedIn with projects",
            ],
            "medium_term": [
                "Complete 2-3 software internships",
                "Achieve a cloud certification (AWS/Azure/GCP)",
                "Build a reputation in an open source project",
                "Develop expertise in a specialised area",
                "Land first full-time software role",
            ],
            "long_term": [
                "Lead technical projects or an engineering team",
                "Architect large-scale systems",
                "Specialise in AI/ML, security, platform, etc.",
                "Mentor junior developers",
                "Consider senior/staff/principal engineering track",
            ],
            "next_steps": [
                "Start a hands-on project this week using your target language",
                "Set up GitHub profile and commit daily",
                "Register for a cloud certification study path",
                "Apply for next available software internship",
                "Solve 3 algorithm problems per day on LeetCode",
            ]
        },
    }

    def _get_profession_plan_data(self, target_profession: str) -> dict:
        """Match profession to the closest plan category"""
        prof_lower = target_profession.lower()
        for category, data in self._PROFESSION_PLANS.items():
            if any(kw in prof_lower for kw in data["keywords"]):
                return data
        # Generic fallback
        return {
            "subjects": [
                f"Core Theory & Fundamentals of {target_profession}",
                "Research Methods & Critical Thinking",
                "Professional Ethics & Standards",
                "Communication & Presentation Skills",
                "Industry Tools & Technologies",
                "Business & Project Management Basics",
            ],
            "activities": f"""**Practical Experience:**
- Internships or work placements in {target_profession} settings
- Volunteering with relevant organisations
- Entry-level or part-time roles in the field

**Clubs & Organizations:**
- Professional associations for {target_profession}
- University clubs related to the field
- Mentorship and networking programs

**Certifications:**
- Industry-recognised certifications for {target_profession}
- Online courses from Coursera, edX, or professional bodies

**Networking:**
- Industry conferences and events
- Connect with established {target_profession} practitioners
- Join LinkedIn groups for the field""",
            "skills": f"""**Technical Skills:**
- Year 1-2: Core knowledge and foundational skills
- Year 2-3: Applied skills and specialisation
- Year 3+: Advanced expertise and leadership

**Soft Skills:**
- Communication and teamwork
- Analytical and problem-solving thinking
- Professionalism and work ethics
- Continuous learning mindset""",
            "education": f"""- **Relevant Degree**: Undergraduate in a related discipline (3-4 years)
- **Professional Qualifications**: As required for {target_profession}
- **Continuing Education**: Industry workshops and short courses
- **Advanced Study** (optional): Postgraduate or master's degree""",
            "short_term": [
                f"Build foundational knowledge in {target_profession}",
                "Gain initial practical or volunteer experience",
                "Identify key certifications or qualifications required",
                "Connect with 2-3 mentors in the field",
                "Develop a personal learning roadmap",
            ],
            "medium_term": [
                "Complete required qualifications or degrees",
                "Accumulate meaningful work experience",
                "Develop a professional portfolio or track record",
                "Achieve industry certifications",
                "Build a professional network in the field",
            ],
            "long_term": [
                f"Establish yourself as a practising {target_profession}",
                "Develop a specialisation or area of expertise",
                "Take on leadership or senior responsibilities",
                "Mentor others entering the field",
                "Contribute to industry advancement",
            ],
            "next_steps": [
                f"Research the exact qualification path for {target_profession} in your country",
                "Identify and reach out to 2 practitioners for informational interviews",
                "Enrol in or audit a foundational course this month",
                "Find a volunteering or shadowing opportunity within 4 weeks",
                "Set 3-month learning goals and review weekly",
            ]
        }

    def _get_career_plan_template(self, target_profession: str) -> Dict:
        """Fallback template for career action plans — profession-aware"""
        d = self._get_profession_plan_data(target_profession)
        subjects_list = "\n".join(f"- {s}" for s in d["subjects"])
        short = "\n".join(f"- ✓ {s}" for s in d["short_term"])
        medium = "\n".join(f"- ✓ {s}" for s in d["medium_term"])
        long_ = "\n".join(f"- ✓ {s}" for s in d["long_term"])
        next_steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(d["next_steps"]))

        plan = f"""## Career Action Plan for {target_profession}

### 1. KEY SUBJECTS TO FOCUS ON (Build Strong Foundation)
{subjects_list}

### 2. KEY ACTIVITIES & EXPERIENCES
{d['activities']}

### 3. SKILL DEVELOPMENT ROADMAP
{d['skills']}

### 4. EDUCATION PATHWAY
{d['education']}

### 5. MILESTONES & TIMELINE

**Short-term (6-12 months):**
{short}

**Medium-term (1-3 years):**
{medium}

**Long-term (3+ years):**
{long_}

### Next Steps:
{next_steps}

Remember: Consistency beats intensity. Dedicate focused time each day and review your progress monthly."""

        return {
            "success": True,
            "response": plan,
            "usage": "template_fallback"
        }


    async def parse_career_plan_to_study_tasks(
        self,
        action_plan: str,
        target_profession: str
    ) -> Dict:
        """Parse career action plan into structured study tasks and schedule"""

        system_prompt = "You are an educational planner who converts career advice into actionable study plans. Extract specific study tasks, subjects, and create a structured learning schedule."

        user_prompt = f"""
        Parse the following career action plan for {target_profession} into a structured study plan format.

        Career Action Plan:
        {action_plan}

        Extract and format the information into the following JSON structure:

        {{
            "study_materials": {{
                "subjects": ["list of key subjects/courses to study"],
                "skills": ["list of technical and soft skills to develop"],
                "resources": ["list of learning resources, books, courses"]
            }},
            "schedule": {{
                "weekly_tasks": [
                    {{
                        "task": "specific study task",
                        "subject": "subject area",
                        "duration": "estimated hours per week",
                        "priority": "high/medium/low",
                        "timeline": "short-term/medium-term/long-term"
                    }}
                ],
                "daily_activities": [
                    {{
                        "activity": "daily practice or learning activity",
                        "duration": "minutes per day",
                        "type": "study/practice/reading"
                    }}
                ]
            }},
            "milestones": {{
                "short_term": ["goals for next 3-6 months"],
                "medium_term": ["goals for 6-18 months"],
                "long_term": ["goals for 1-3 years"]
            }},
            "tasks": [
                {{
                    "id": 1,
                    "title": "specific actionable task",
                    "description": "detailed description",
                    "category": "study/skill/activity/networking",
                    "estimated_hours": 5,
                    "priority": "high/medium/low",
                    "deadline": "timeframe description"
                }}
            ]
        }}

        Extract at least 8-12 specific, actionable study tasks. Be practical and realistic about time estimates.
        Focus on tasks that can be integrated into a weekly study schedule.
        """

        return await self._generate_response(user_prompt, system_prompt)

# Create service instance
ai_service = AIAssistantService()