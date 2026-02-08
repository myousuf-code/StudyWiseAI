"""
Progress Tracking API Routes
Monitor learning progress with analytics and insights
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.database import User, ProgressRecord, StudySession

router = APIRouter()

# Pydantic models
class ProgressRecordCreate(BaseModel):
    subject: str
    topic: str
    time_spent: int  # minutes
    sessions_completed: int
    accuracy_score: Optional[float] = None
    difficulty_level: str

class ProgressRecordResponse(BaseModel):
    id: int
    date: datetime
    subject: str
    topic: str
    time_spent: int
    sessions_completed: int
    accuracy_score: Optional[float]
    retention_score: Optional[float]
    difficulty_level: str
    learning_patterns: Optional[Dict]
    recommendations: Optional[Dict]
    
    class Config:
        from_attributes = True

class ProgressSummary(BaseModel):
    total_study_time: int  # minutes
    total_sessions: int
    subjects_studied: List[str]
    average_accuracy: float
    current_streak: int  # days
    weekly_progress: List[Dict]
    learning_trends: Dict

class StudySessionUpdate(BaseModel):
    actual_duration: Optional[int] = None
    end_time: Optional[datetime] = None
    focus_score: Optional[float] = None
    completion_rate: Optional[float] = None
    notes: Optional[str] = None

@router.post("/", response_model=ProgressRecordResponse)
async def create_progress_record(
    record: ProgressRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new progress record"""
    
    db_record = ProgressRecord(
        user_id=current_user.id,
        subject=record.subject,
        topic=record.topic,
        time_spent=record.time_spent,
        sessions_completed=record.sessions_completed,
        accuracy_score=record.accuracy_score,
        difficulty_level=record.difficulty_level,
        # AI will calculate retention score and patterns later
        learning_patterns={"recorded_at": datetime.utcnow().isoformat()},
        recommendations={"type": "basic"}
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record

@router.get("/", response_model=List[ProgressRecordResponse])
async def get_progress_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    subject: Optional[str] = None,
    days: int = 30
):
    """Get progress records for the current user"""
    
    # Calculate date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.date >= start_date
    )
    
    if subject:
        query = query.filter(ProgressRecord.subject == subject)
    
    records = query.order_by(desc(ProgressRecord.date)).all()
    return records

@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Get comprehensive progress summary"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get progress records
    records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.date >= start_date
    ).all()
    
    if not records:
        return ProgressSummary(
            total_study_time=0,
            total_sessions=0,
            subjects_studied=[],
            average_accuracy=0.0,
            current_streak=0,
            weekly_progress=[],
            learning_trends={}
        )
    
    # Calculate summary statistics
    total_time = sum(r.time_spent for r in records)
    total_sessions = sum(r.sessions_completed for r in records)
    subjects = list(set(r.subject for r in records))
    avg_accuracy = sum(r.accuracy_score or 0 for r in records) / len(records)
    
    # Calculate current streak
    current_streak = calculate_study_streak(current_user.id, db)
    
    # Weekly progress breakdown
    weekly_progress = calculate_weekly_progress(records)
    
    # Learning trends
    learning_trends = analyze_learning_trends(records)
    
    return ProgressSummary(
        total_study_time=total_time,
        total_sessions=total_sessions,
        subjects_studied=subjects,
        average_accuracy=avg_accuracy,
        current_streak=current_streak,
        weekly_progress=weekly_progress,
        learning_trends=learning_trends
    )

@router.get("/analytics")
async def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    period: str = "month"  # week, month, year
):
    """Get detailed analytics for progress visualization"""
    
    if period == "week":
        days = 7
    elif period == "month":
        days = 30
    elif period == "year":
        days = 365
    else:
        days = 30
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily study time
    daily_time = db.query(
        func.date(ProgressRecord.date).label('date'),
        func.sum(ProgressRecord.time_spent).label('total_time')
    ).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.date >= start_date
    ).group_by(func.date(ProgressRecord.date)).all()
    
    # Subject distribution
    subject_dist = db.query(
        ProgressRecord.subject,
        func.sum(ProgressRecord.time_spent).label('time_spent'),
        func.count(ProgressRecord.id).label('session_count')
    ).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.date >= start_date
    ).group_by(ProgressRecord.subject).all()
    
    # Accuracy trends
    accuracy_trends = db.query(
        func.date(ProgressRecord.date).label('date'),
        func.avg(ProgressRecord.accuracy_score).label('avg_accuracy')
    ).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.date >= start_date,
        ProgressRecord.accuracy_score.isnot(None)
    ).group_by(func.date(ProgressRecord.date)).all()
    
    return {
        "daily_time": [{"date": str(d.date), "minutes": d.total_time} for d in daily_time],
        "subject_distribution": [
            {"subject": s.subject, "time_spent": s.time_spent, "sessions": s.session_count}
            for s in subject_dist
        ],
        "accuracy_trends": [
            {"date": str(a.date), "accuracy": float(a.avg_accuracy)}
            for a in accuracy_trends
        ],
        "period": period
    }

@router.put("/sessions/{session_id}")
async def update_study_session(
    session_id: int,
    session_update: StudySessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a study session with completion data"""
    
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found"
        )
    
    # Update fields
    for field, value in session_update.dict(exclude_none=True).items():
        setattr(session, field, value)
    
    # Update status based on completion
    if session_update.end_time:
        session.status = "completed"
    
    db.commit()
    db.refresh(session)
    
    # Create progress record if session is completed
    if session.status == "completed" and session.actual_duration:
        progress_record = ProgressRecord(
            user_id=current_user.id,
            subject=session.study_plan.subject if session.study_plan else "General",
            topic=session.title,
            time_spent=session.actual_duration,
            sessions_completed=1,
            accuracy_score=session_update.completion_rate,
            difficulty_level="intermediate"  # Default
        )
        db.add(progress_record)
        db.commit()
    
    return {"message": "Session updated successfully", "session": session}

# Helper functions
def calculate_study_streak(user_id: int, db: Session) -> int:
    """Calculate current consecutive study days streak"""
    today = datetime.utcnow().date()
    streak = 0
    current_date = today
    
    while True:
        # Check if user studied on current_date
        has_session = db.query(ProgressRecord).filter(
            ProgressRecord.user_id == user_id,
            func.date(ProgressRecord.date) == current_date
        ).first()
        
        if has_session:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def calculate_weekly_progress(records: List[ProgressRecord]) -> List[Dict]:
    """Calculate weekly progress breakdown"""
    weekly_data = {}
    
    for record in records:
        week_start = record.date.date() - timedelta(days=record.date.weekday())
        week_key = week_start.isoformat()
        
        if week_key not in weekly_data:
            weekly_data[week_key] = {"time": 0, "sessions": 0, "subjects": set()}
        
        weekly_data[week_key]["time"] += record.time_spent
        weekly_data[week_key]["sessions"] += record.sessions_completed
        weekly_data[week_key]["subjects"].add(record.subject)
    
    return [
        {
            "week_start": week,
            "time_spent": data["time"],
            "sessions": data["sessions"],
            "subjects_count": len(data["subjects"])
        }
        for week, data in sorted(weekly_data.items())
    ]

def analyze_learning_trends(records: List[ProgressRecord]) -> Dict:
    """Analyze learning trends and patterns"""
    if not records:
        return {}
    
    # Most studied subjects
    subject_time = {}
    for record in records:
        subject_time[record.subject] = subject_time.get(record.subject, 0) + record.time_spent
    
    most_studied = sorted(subject_time.items(), key=lambda x: x[1], reverse=True)
    
    # Study consistency (days with study sessions)
    study_days = len(set(record.date.date() for record in records))
    total_days = (max(record.date for record in records) - min(record.date for record in records)).days + 1
    consistency = (study_days / total_days) * 100 if total_days > 0 else 0
    
    return {
        "most_studied_subjects": most_studied[:3],
        "study_consistency": round(consistency, 1),
        "average_session_length": sum(r.time_spent for r in records) / len(records),
        "total_subjects": len(set(r.subject for r in records))
    }