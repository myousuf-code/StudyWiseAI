"""
Study Plans API Routes
Manage AI-generated personalized study plans
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.database import User, StudyPlan, StudySession
from app.services.ai_service import ai_service

router = APIRouter()

# Pydantic models
class StudyPlanCreate(BaseModel):
    title: str
    description: str
    subject: str
    difficulty_level: str
    estimated_duration: int
    study_materials: Optional[Dict] = None
    schedule: Optional[Dict] = None
    milestones: Optional[Dict] = None

class StudyPlanResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    difficulty_level: str
    estimated_duration: int
    created_at: datetime
    is_active: bool
    study_materials: Optional[Dict] = None
    schedule: Optional[Dict] = None
    milestones: Optional[Dict] = None
    
    class Config:
        from_attributes = True

class StudySessionCreate(BaseModel):
    study_plan_id: Optional[int] = None
    title: str
    duration: int  # in minutes
    topics_covered: Optional[List[str]] = None

class StudySessionResponse(BaseModel):
    id: int
    title: str
    duration: int
    actual_duration: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    focus_score: Optional[float]
    completion_rate: Optional[float]
    notes: Optional[str]
    topics_covered: Optional[Dict]
    
    class Config:
        from_attributes = True

@router.post("/", response_model=StudyPlanResponse)
async def create_study_plan(
    plan: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new study plan"""
    
    db_plan = StudyPlan(
        user_id=current_user.id,
        title=plan.title,
        description=plan.description,
        subject=plan.subject,
        difficulty_level=plan.difficulty_level,
        estimated_duration=plan.estimated_duration,
        study_materials=plan.study_materials,
        schedule=plan.schedule,
        milestones=plan.milestones
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.get("/", response_model=List[StudyPlanResponse])
async def get_study_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    active_only: bool = True
):
    """Get all study plans for the current user"""
    
    query = db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id)
    
    if active_only:
        query = query.filter(StudyPlan.is_active == True)
    
    plans = query.order_by(StudyPlan.created_at.desc()).all()
    return plans

@router.get("/{plan_id}", response_model=StudyPlanResponse)
async def get_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific study plan"""
    
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found"
        )
    
    return plan

@router.put("/{plan_id}", response_model=StudyPlanResponse)
async def update_study_plan(
    plan_id: int,
    plan_update: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a study plan"""
    
    db_plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found"
        )
    
    # Update fields
    for field, value in plan_update.dict().items():
        if value is not None:
            setattr(db_plan, field, value)
    
    db_plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.delete("/{plan_id}")
async def delete_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete (deactivate) a study plan"""
    
    db_plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found"
        )
    
    db_plan.is_active = False
    db.commit()
    
    return {"message": "Study plan deactivated successfully"}

@router.post("/{plan_id}/sessions", response_model=StudySessionResponse)
async def create_study_session(
    plan_id: int,
    session: StudySessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new study session for a plan"""
    
    # Verify plan belongs to user
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found"
        )
    
    db_session = StudySession(
        user_id=current_user.id,
        study_plan_id=plan_id,
        title=session.title,
        duration=session.duration,
        topics_covered={"topics": session.topics_covered} if session.topics_covered else None
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session

@router.get("/{plan_id}/sessions", response_model=List[StudySessionResponse])
async def get_plan_sessions(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all sessions for a study plan"""
    
    # Verify plan belongs to user
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found"
        )
    
    sessions = db.query(StudySession).filter(
        StudySession.study_plan_id == plan_id
    ).order_by(StudySession.start_time.desc()).all()
    
    return sessions

@router.post("/ai-generate")
async def generate_ai_study_plan(
    subject: str,
    duration_weeks: int,
    difficulty_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a study plan using AI"""
    
    ai_response = await ai_service.generate_study_plan(
        user=current_user,
        subject=subject,
        duration_weeks=duration_weeks,
        difficulty_level=difficulty_level,
        learning_style=current_user.learning_style or "mixed"
    )
    
    if not ai_response["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate AI study plan"
        )
    
    # Create the study plan in database
    db_plan = StudyPlan(
        user_id=current_user.id,
        title=f"AI Study Plan: {subject}",
        description=f"AI-generated {duration_weeks}-week study plan for {subject}",
        subject=subject,
        difficulty_level=difficulty_level,
        estimated_duration=duration_weeks * 7 * 60,  # weeks * days * minutes per day
        study_materials={"ai_generated": True},
        schedule={"plan": ai_response["plan"]},
        milestones={"ai_generated": True}
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return {
        "plan": db_plan,
        "ai_content": ai_response["response"]  # Changed from "plan" to "response"
    }