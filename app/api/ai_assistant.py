"""
AI Assistant API Routes
Chat interface and AI-powered study assistance
"""
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.config import settings
from app.models.database import User, ChatMessage, ProgressRecord, CareerCounselingSession
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    message_type: str

class StudyPlanRequest(BaseModel):
    subject: str
    duration_weeks: int
    difficulty_level: str  # beginner, intermediate, advanced

class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    question_count: int = 5

class CareerCounselingRequest(BaseModel):
    target_profession: str

class CareerActionPlanRequest(BaseModel):
    target_profession: str
    user_responses: str

class ConvertCareerToStudyPlanRequest(BaseModel):
    session_id: int
    plan_title: Optional[str] = None

@router.get("/status")
async def ai_status(
    current_user: User = Depends(get_current_user)
):
    """Check AI provider status"""
    if ai_service._groq_client:
        return {
            "status": "ready",
            "provider": "groq",
            "model_loaded": True,
            "model_loading": False,
            "model_name": settings.GROQ_MODEL,
            "message": f"Groq API ready ({settings.GROQ_MODEL})",
        }
    if ai_service._model is not None:
        status = "ready"
        provider = "local"
        message = f"Local model ready ({ai_service._model_name_in_use})"
    elif ai_service._model_loading:
        status = "loading"
        provider = "local"
        message = "Local AI model is loading/downloading automatically"
    else:
        status = "failed"
        provider = "none"
        message = "No AI provider available — set GROQ_API_KEY in .env for instant access"
    return {
        "status": status,
        "provider": provider,
        "model_available": ai_service.is_model_available,
        "model_loaded": ai_service._model is not None,
        "model_loading": ai_service._model_loading,
        "model_name": ai_service._model_name_in_use,
        "message": message,
    }


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI assistant for study help"""
    
    # Get AI response
    ai_response = await ai_service.get_study_help(
        user=current_user,
        question=request.message,
        context=request.context
    )
    
    if not ai_response["success"]:
        logger.error("AI chat service error for user %s: %s", current_user.id, ai_response.get("error"))
        raise HTTPException(status_code=500, detail="AI service is temporarily unavailable. Please try again.")
    
    # Save chat message to database
    chat_message = ChatMessage(
        user_id=current_user.id,
        message=request.message,
        response=ai_response["response"],
        message_type="study_help",
        context_data=request.context,
        confidence_score=ai_response.get("confidence", None)
    )
    
    db.add(chat_message)
    db.commit()
    
    return ChatResponse(
        response=ai_response["response"],
        timestamp=datetime.now(timezone.utc),
        message_type="study_help"
    )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Streaming chat endpoint using Server-Sent Events.
    Sends tokens as they are generated so the UI can display them immediately.
    Final event saves the message to the database.
    """
    system_prompt = (
        "You are a helpful AI tutor who provides clear, encouraging study assistance. "
        "Give practical, educational answers that help students learn effectively."
    )

    context_info = ""
    if request.context and request.context.get("current_topic"):
        context_info = f"Currently studying: {request.context['current_topic']}\n"
    if current_user.learning_style:
        context_info += f"Learning style: {current_user.learning_style}\n"

    user_prompt = (
        f"{context_info}Student Question: {request.message}\n\n"
        "Please provide a helpful, educational response. Keep it concise but thorough."
    )

    full_response_parts: list[str] = []

    async def event_stream():
        try:
            async for token in ai_service.stream_response(user_prompt, system_prompt):
                full_response_parts.append(token)
                yield f"data: {json.dumps({'token': token})}\n\n"

            full_text = "".join(full_response_parts).strip()

            # Persist to DB after streaming completes
            chat_message = ChatMessage(
                user_id=current_user.id,
                message=request.message,
                response=full_text,
                message_type="study_help",
                context_data=request.context,
                confidence_score=None,
            )
            db.add(chat_message)
            db.commit()

            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            logger.error("Streaming error for user %s: %s", current_user.id, e)
            yield f"data: {json.dumps({'error': 'Streaming error occurred'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.post("/generate-study-plan")
async def generate_study_plan(
    request: StudyPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered personalized study plan"""
    
    ai_response = await ai_service.generate_study_plan(
        user=current_user,
        subject=request.subject,
        duration_weeks=request.duration_weeks,
        difficulty_level=request.difficulty_level,
        learning_style=current_user.learning_style or "mixed"
    )
    
    if not ai_response["success"]:
        raise HTTPException(status_code=500, detail="Failed to generate study plan")
    
    return {
        "plan": ai_response["response"],
        "subject": request.subject,
        "duration_weeks": request.duration_weeks,
        "difficulty_level": request.difficulty_level
    }

@router.get("/progress-insights")
async def get_progress_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered insights about user's progress"""
    
    # Get user's progress records
    progress_records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id
    ).order_by(ProgressRecord.date.desc()).limit(20).all()
    
    ai_response = await ai_service.analyze_progress(
        user=current_user,
        progress_records=progress_records
    )
    
    if not ai_response["success"]:
        raise HTTPException(status_code=500, detail="Failed to analyze progress")
    
    return {
        "insights": ai_response["insights"],
        "total_sessions": len(progress_records),
        "analysis_date": datetime.now(timezone.utc)
    }

@router.post("/generate-quiz")
async def generate_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate quiz questions for a topic"""
    
    ai_response = await ai_service.generate_quiz_questions(
        topic=request.topic,
        difficulty=request.difficulty,
        question_count=request.question_count
    )
    
    if not ai_response["success"]:
        raise HTTPException(status_code=500, detail="Failed to generate quiz")
    
    return {
        "questions": ai_response["questions"],
        "topic": request.topic,
        "difficulty": request.difficulty,
        "question_count": request.question_count
    }

@router.post("/career-counseling/start")
async def start_career_counseling(
    request: CareerCounselingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a career counseling session by asking initial questions"""
    import asyncio
    
    try:
        logger.info("Starting career counseling session for user %s, profession: %s", current_user.id, request.target_profession)

        # Add timeout to prevent hanging - much shorter with faster model
        ai_response = await asyncio.wait_for(
            ai_service.start_career_counseling(
                user=current_user,
                target_profession=request.target_profession
            ),
            timeout=60.0  # 60 seconds for first model load
        )

        logger.debug("Career counseling AI response received: %d chars", len(ai_response.get("response", "")))

        if not ai_response["success"]:
            logger.error("Career counseling AI error for user %s: %s", current_user.id, ai_response.get("error"))
            raise HTTPException(status_code=500, detail="Failed to start career counseling session. Please try again.")

        # Save career counseling session to database
        career_session = CareerCounselingSession(
            user_id=current_user.id,
            target_profession=request.target_profession,
            initial_questions=ai_response["response"],
            session_status="active"
        )

        db.add(career_session)
        db.commit()
        db.refresh(career_session)

        logger.info("Career counseling session saved with ID: %s", career_session.id)

        return {
            "session_id": career_session.id,
            "target_profession": request.target_profession,
            "initial_questions": ai_response["response"],
            "session_started": career_session.created_at
        }
    except asyncio.TimeoutError:
        logger.warning("Career counseling timeout for user %s", current_user.id)
        raise HTTPException(
            status_code=504,
            detail="AI model is taking longer than expected. The system may be busy. Please try again in a moment."
        )
    except Exception as e:
        logger.exception("Unexpected error in career counseling start for user %s", current_user.id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")

@router.post("/career-counseling/generate-plan")
async def generate_career_action_plan(
    request: CareerActionPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a comprehensive career action plan based on user responses"""
    import asyncio
    
    try:
        logger.info("Generating career plan for user %s, profession: %s", current_user.id, request.target_profession)

        # Add timeout to prevent hanging
        ai_response = await asyncio.wait_for(
            ai_service.generate_career_action_plan(
                user=current_user,
                target_profession=request.target_profession,
                user_responses=request.user_responses
            ),
            timeout=600.0  # 10 minute timeout for local AI model generation on slow hardware
        )

        logger.debug("Career plan AI response received: %d chars", len(ai_response.get("response", "")))

        if not ai_response["success"]:
            logger.error("Career plan AI error for user %s: %s", current_user.id, ai_response.get("error"))
            raise HTTPException(status_code=500, detail="Failed to generate career action plan. Please try again.")

        # Update or create career counseling session
        career_session = db.query(CareerCounselingSession).filter(
            CareerCounselingSession.user_id == current_user.id,
            CareerCounselingSession.target_profession == request.target_profession,
            CareerCounselingSession.session_status == "active"
        ).first()

        if career_session:
            career_session.user_responses = request.user_responses
            career_session.action_plan = ai_response["response"]
            career_session.session_status = "completed"
            career_session.updated_at = datetime.now(timezone.utc)
        else:
            # Create new session if none exists
            career_session = CareerCounselingSession(
                user_id=current_user.id,
                target_profession=request.target_profession,
                user_responses=request.user_responses,
                action_plan=ai_response["response"],
                session_status="completed"
            )
            db.add(career_session)

        db.commit()
        db.refresh(career_session)

        logger.info("Career plan saved with session ID: %s", career_session.id)

        return {
            "session_id": career_session.id,
            "target_profession": request.target_profession,
            "action_plan": ai_response["response"],
            "generated_at": career_session.updated_at
        }
    except asyncio.TimeoutError:
        logger.warning("Career plan generation timeout for user %s", current_user.id)
        raise HTTPException(status_code=504, detail="AI model is taking too long to respond. Please try again in a moment.")
    except Exception as e:
        logger.exception("Unexpected error generating career plan for user %s", current_user.id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")

@router.get("/career-counseling/history")
async def get_career_counseling_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's career counseling session history"""

    sessions = db.query(CareerCounselingSession).filter(
        CareerCounselingSession.user_id == current_user.id
    ).order_by(CareerCounselingSession.created_at.desc()).all()

    return [
        {
            "session_id": session.id,
            "target_profession": session.target_profession,
            "session_status": session.session_status,
            "created_at": session.created_at,
            "has_action_plan": session.action_plan is not None,
            "initial_questions": session.initial_questions,
            "action_plan": session.action_plan
        }
        for session in sessions
    ]

@router.post("/career-counseling/convert-to-study-plan")
async def convert_career_to_study_plan(
    request: ConvertCareerToStudyPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Convert career counseling action plan to study plan tasks"""
    
    # Get the career session
    career_session = db.query(CareerCounselingSession).filter(
        CareerCounselingSession.id == request.session_id,
        CareerCounselingSession.user_id == current_user.id
    ).first()
    
    if not career_session or not career_session.action_plan:
        raise HTTPException(status_code=404, detail="Career session or action plan not found")
    
    try:
        # Build structured study plan data directly from the action plan text
        # (skips AI parsing which is slow/unreliable - the plan is already well-structured)
        import re
        action_plan_text = career_session.action_plan
        profession = career_session.target_profession

        def extract_bullet_lines(section_text: str) -> list:
            """Extract non-empty lines that look like bullet points or list items"""
            lines = []
            for line in section_text.splitlines():
                line = line.strip().lstrip("-•*").strip()
                line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)  # remove bold markdown
                if line and len(line) > 3:
                    lines.append(line)
            return lines

        # Extract subjects section
        subjects_match = re.search(r"KEY SUBJECTS.*?\n(.*?)(?=###|\Z)", action_plan_text, re.S | re.I)
        subjects = extract_bullet_lines(subjects_match.group(1))[:8] if subjects_match else []

        # Extract milestones
        short_match = re.search(r"Short-term.*?\n(.*?)(?=\n\*\*Medium|\n###|\Z)", action_plan_text, re.S | re.I)
        medium_match = re.search(r"Medium-term.*?\n(.*?)(?=\n\*\*Long|\n###|\Z)", action_plan_text, re.S | re.I)
        long_match = re.search(r"Long-term.*?\n(.*?)(?=\n###|Next Steps|\Z)", action_plan_text, re.S | re.I)

        short_term = extract_bullet_lines(short_match.group(1))[:5] if short_match else []
        medium_term = extract_bullet_lines(medium_match.group(1))[:5] if medium_match else []
        long_term = extract_bullet_lines(long_match.group(1))[:5] if long_match else []

        # Build weekly tasks from subjects
        weekly_tasks = [
            {"task": f"Study {s}", "subject": s, "duration": "3-5 hours/week", "priority": "high" if i < 3 else "medium", "timeline": "short-term"}
            for i, s in enumerate(subjects)
        ]

        # Build actionable tasks list from short + medium term goals
        tasks = []
        for i, goal in enumerate((short_term + medium_term)[:12], start=1):
            tasks.append({
                "id": i,
                "title": goal,
                "description": f"Complete as part of your {profession} career path",
                "category": "study",
                "estimated_hours": 5,
                "priority": "high" if i <= 5 else "medium",
                "deadline": "short-term" if i <= len(short_term) else "medium-term"
            })

        parsed_data = {
            "study_materials": {
                "subjects": subjects,
                "skills": extract_bullet_lines(
                    re.search(r"SKILL DEVELOPMENT.*?\n(.*?)(?=###|\Z)", action_plan_text, re.S | re.I).group(1)
                )[:8] if re.search(r"SKILL DEVELOPMENT.*?\n(.*?)(?=###|\Z)", action_plan_text, re.S | re.I) else [],
                "resources": ["Coursera", "Udemy", "Khan Academy", "YouTube tutorials", "Official documentation"]
            },
            "schedule": {
                "weekly_tasks": weekly_tasks,
                "daily_activities": [
                    {"activity": f"Review {profession} study materials", "duration": "30", "type": "study"},
                    {"activity": "Practice problems or exercises", "duration": "45", "type": "practice"},
                ]
            },
            "milestones": {
                "short_term": short_term or [f"Build foundation in {profession} core subjects"],
                "medium_term": medium_term or [f"Gain practical experience in {profession}"],
                "long_term": long_term or [f"Establish career as {profession}"]
            },
            "tasks": tasks
        }

        # Create study plan from parsed data
        from app.models.database import StudyPlan
        
        plan_title = request.plan_title or f"Career Path: {career_session.target_profession}"
        
        study_plan = StudyPlan(
            user_id=current_user.id,
            title=plan_title,
            description=f"Study plan derived from career counseling for {career_session.target_profession}",
            subject="Career Development",
            difficulty_level="intermediate",
            estimated_duration=0,  # Will be calculated from tasks
            study_materials=parsed_data.get("study_materials", {}),
            schedule=parsed_data.get("schedule", {}),
            milestones=parsed_data.get("milestones", {})
        )
        
        # Add career counseling reference to the study plan
        if not study_plan.study_materials:
            study_plan.study_materials = {}
        study_plan.study_materials["career_source"] = {
            "session_id": career_session.id,
            "target_profession": career_session.target_profession,
            "generated_from": "career_counseling"
        }
        
        db.add(study_plan)
        db.commit()
        db.refresh(study_plan)
        
        return {
            "success": True,
            "study_plan_id": study_plan.id,
            "title": study_plan.title,
            "tasks_created": len(parsed_data.get("tasks", [])),
            "schedule": study_plan.schedule,
            "message": f"Successfully converted career plan to study plan with {len(parsed_data.get('tasks', []))} tasks"
        }
        
    except Exception as e:
        logger.exception("Error converting career plan to study plan for user %s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to convert career plan to study plan. Please try again.")

class NLPRequest(BaseModel):
    text: str

@router.post("/summarize")
async def summarize_text(
    request: NLPRequest,
    current_user: User = Depends(get_current_user),
):
    """Summarize text using the local AI model"""
    import asyncio
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    try:
        result = await asyncio.wait_for(
            ai_service.summarize_text(request.text),
            timeout=120.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="AI model timed out. Please try again.")
    if not result["success"]:
        logger.error("Summarize failed for user %s: %s", current_user.id, result.get("error"))
        raise HTTPException(status_code=500, detail="Failed to summarize text. Please try again.")
    return {"summary": result["response"]}

@router.post("/sentiment")
async def analyze_sentiment(
    request: NLPRequest,
    current_user: User = Depends(get_current_user),
):
    """Analyze the sentiment of the provided text"""
    import asyncio
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    try:
        result = await asyncio.wait_for(
            ai_service.analyze_sentiment(request.text),
            timeout=120.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="AI model timed out. Please try again.")
    if not result["success"]:
        logger.error("Sentiment analysis failed for user %s: %s", current_user.id, result.get("error"))
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment. Please try again.")
    return {"sentiment": result["response"]}

@router.post("/grammar")
async def check_grammar(
    request: NLPRequest,
    current_user: User = Depends(get_current_user),
):
    """Check grammar and writing quality of the provided text"""
    import asyncio
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    try:
        result = await asyncio.wait_for(
            ai_service.check_grammar(request.text),
            timeout=120.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="AI model timed out. Please try again.")
    if not result["success"]:
        logger.error("Grammar check failed for user %s: %s", current_user.id, result.get("error"))
        raise HTTPException(status_code=500, detail="Failed to check grammar. Please try again.")
    return {"result": result["response"]}

@router.post("/paraphrase")
async def paraphrase_text(
    request: NLPRequest,
    current_user: User = Depends(get_current_user),
):
    """Paraphrase the provided text"""
    import asyncio
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    try:
        result = await asyncio.wait_for(
            ai_service.paraphrase_text(request.text),
            timeout=120.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="AI model timed out. Please try again.")
    if not result["success"]:
        logger.error("Paraphrase failed for user %s: %s", current_user.id, result.get("error"))
        raise HTTPException(status_code=500, detail="Failed to paraphrase text. Please try again.")
    return {"paraphrase": result["response"]}

@router.get("/chat-history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get user's chat history with AI assistant"""
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "message": msg.message,
            "response": msg.response,
            "timestamp": msg.timestamp,
            "message_type": msg.message_type
        }
        for msg in messages
    ]