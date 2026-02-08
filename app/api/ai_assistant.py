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
from app.models.database import User, ChatMessage, ProgressRecord
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