"""
AI Assistant API Routes
Chat interface and AI-powered study assistance
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.database import User, ChatMessage, ProgressRecord, CareerCounselingSession
from app.services.ai_service import ai_service

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
        raise HTTPException(status_code=500, detail=f"AI service error: {ai_response.get('error', 'Unknown error')}")
    
    # Save chat message to database
    chat_message = ChatMessage(
        user_id=current_user.id,
        message=request.message,
        response=ai_response["response"],
        message_type="study_help",
        context_data=request.context,
        confidence_score=0.8  # Default confidence for local models
    )
    
    db.add(chat_message)
    db.commit()
    
    return ChatResponse(
        response=ai_response["response"],
        timestamp=datetime.utcnow(),
        message_type="study_help"
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
        "plan": ai_response["plan"],
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
        "analysis_date": datetime.utcnow()
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
        print(f"[Career Counseling] Starting session for profession: {request.target_profession}")
        
        # Add timeout to prevent hanging - much shorter with faster model
        ai_response = await asyncio.wait_for(
            ai_service.start_career_counseling(
                user=current_user,
                target_profession=request.target_profession
            ),
            timeout=60.0  # Increased to 60 seconds for first model load
        )
        
        print(f"[Career Counseling] AI response received: {len(ai_response.get('response', ''))} chars")

        if not ai_response["success"]:
            error_msg = ai_response.get("error", "Unknown error")
            print(f"[Career Counseling] AI service error: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Failed to start career counseling: {error_msg}")

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
        
        print(f"[Career Counseling] Session saved with ID: {career_session.id}")

        return {
            "session_id": career_session.id,
            "target_profession": request.target_profession,
            "initial_questions": ai_response["response"],
            "session_started": career_session.created_at
        }
    except asyncio.TimeoutError:
        print("[Career Counseling] Request timeout - AI model took too long to respond")
        raise HTTPException(
            status_code=504, 
            detail="AI model is taking longer than expected. The system may be busy. Please try again in a moment."
        )
    except Exception as e:
        print(f"[Career Counseling] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/career-counseling/generate-plan")
async def generate_career_action_plan(
    request: CareerActionPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a comprehensive career action plan based on user responses"""
    import asyncio
    
    try:
        print(f"[Career Plan] Generating plan for profession: {request.target_profession}")
        
        # Add timeout to prevent hanging
        ai_response = await asyncio.wait_for(
            ai_service.generate_career_action_plan(
                user=current_user,
                target_profession=request.target_profession,
                user_responses=request.user_responses
            ),
            timeout=600.0  # 10 minute timeout for local AI model generation on slow hardware
        )
        
        print(f"[Career Plan] AI response received: {len(ai_response.get('response', ''))} chars")

        if not ai_response["success"]:
            error_msg = ai_response.get("error", "Unknown error")
            print(f"[Career Plan] AI service error: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Failed to generate career action plan: {error_msg}")

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
            career_session.updated_at = datetime.utcnow()
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
        
        print(f"[Career Plan] Plan saved with session ID: {career_session.id}")

        return {
            "session_id": career_session.id,
            "target_profession": request.target_profession,
            "action_plan": ai_response["response"],
            "generated_at": career_session.updated_at
        }
    except asyncio.TimeoutError:
        print("[Career Plan] Request timeout - AI model took too long to respond")
        raise HTTPException(status_code=504, detail="AI model is taking too long to respond. Please try again in a moment.")
    except Exception as e:
        print(f"[Career Plan] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

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
        print(f"Error converting career plan to study plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to convert career plan: {str(e)}")

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

# WebSocket endpoint for real-time chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/chat-ws")
async def websocket_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time AI chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Note: In production, you'd want to authenticate the WebSocket connection
            # For now, we'll skip authentication in WebSocket
            
            # Process message with AI
            # This is simplified - you'd want to parse the JSON and extract user info
            ai_response = await ai_service.get_study_help(
                user=None,  # Would need to get user from WebSocket auth
                question=data,
                context=None
            )
            
            if ai_response["success"]:
                await manager.send_personal_message(ai_response["response"], websocket)
            else:
                await manager.send_personal_message("Sorry, I couldn't process that request.", websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)