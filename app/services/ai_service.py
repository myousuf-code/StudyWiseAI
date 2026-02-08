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

class AIAssistantService:
    """Service class for local AI-powered study assistance using GPT4All"""
    
    def __init__(self):
        # Use a lightweight model that's good for educational content
        self.model_name = "orca-mini-3b-gguf2-q4_0.gguf"  # Small but capable model
        self._model = None
        
    def _get_model(self):
        """Lazy load the model to avoid loading it on import"""
        if self._model is None:
            try:
                print("Loading local AI model (this may take a few minutes on first run)...")
                self._model = GPT4All(self.model_name)
                print("✅ Local AI model loaded successfully!")
            except Exception as e:
                print(f"❌ Failed to load AI model: {e}")
                print("💡 The model will be downloaded automatically on first use")
                self._model = GPT4All(self.model_name)
        return self._model
        
    async def _generate_response(self, prompt: str, system_prompt: str = None) -> Dict:
        """Generate response using local GPT4All model"""
        try:
            # Prepare the full prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
                
            # Run model generation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            model = self._get_model()
            
            def generate():
                with model.chat_session():
                    response = model.generate(
                        full_prompt, 
                        max_tokens=800,
                        temp=0.7,
                        top_p=0.9
                    )
                    return response
            
            response = await loop.run_in_executor(None, generate)
            
            return {
                "success": True,
                "response": response.strip(),
                "usage": "local"  # No token usage for local models
            }
                
        except Exception as e:
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

# Create service instance
ai_service = AIAssistantService()