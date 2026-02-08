"""
Smart Reminders API Routes
Intelligent notifications and study session reminders
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.database import User, Reminder

router = APIRouter()

# Pydantic models
class ReminderCreate(BaseModel):
    title: str
    message: str
    reminder_type: str  # study_session, break, review, custom
    scheduled_time: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly

class ReminderResponse(BaseModel):
    id: int
    title: str
    message: str
    reminder_type: str
    scheduled_time: datetime
    is_sent: bool
    is_recurring: bool
    recurrence_pattern: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None

@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create a new reminder"""
    
    # Validate scheduled time is in the future
    if reminder.scheduled_time <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduled time must be in the future"
        )
    
    db_reminder = Reminder(
        user_id=current_user.id,
        title=reminder.title,
        message=reminder.message,
        reminder_type=reminder.reminder_type,
        scheduled_time=reminder.scheduled_time,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern
    )
    
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    # Schedule the reminder (in production, use Celery or similar)
    background_tasks.add_task(schedule_reminder_notification, db_reminder.id)
    
    return db_reminder

@router.get("/", response_model=List[ReminderResponse])
async def get_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    upcoming_only: bool = True
):
    """Get all reminders for the current user"""
    
    query = db.query(Reminder).filter(Reminder.user_id == current_user.id)
    
    if upcoming_only:
        query = query.filter(Reminder.scheduled_time > datetime.utcnow())
    
    reminders = query.order_by(Reminder.scheduled_time.asc()).all()
    return reminders

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific reminder"""
    
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    return reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a reminder"""
    
    db_reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Update fields
    for field, value in reminder_update.dict(exclude_none=True).items():
        setattr(db_reminder, field, value)
    
    db.commit()
    db.refresh(db_reminder)
    
    return db_reminder

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a reminder"""
    
    db_reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    db.delete(db_reminder)
    db.commit()
    
    return {"message": "Reminder deleted successfully"}

@router.post("/study-session")
async def create_study_session_reminder(
    title: str,
    duration_minutes: int,
    start_time: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a reminder for a study session"""
    
    if start_time <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be in the future"
        )
    
    # Create reminder 10 minutes before study session
    reminder_time = start_time - timedelta(minutes=10)
    
    db_reminder = Reminder(
        user_id=current_user.id,
        title=f"Study Session: {title}",
        message=f"Your {duration_minutes}-minute study session '{title}' starts in 10 minutes!",
        reminder_type="study_session",
        scheduled_time=reminder_time
    )
    
    db.add(db_reminder)
    db.commit()
    
    return {"message": "Study session reminder created", "reminder_time": reminder_time}

@router.post("/break-reminder")
async def create_break_reminder(
    study_duration: int,  # minutes
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a break reminder during study session"""
    
    # Create break reminder for after the study duration
    break_time = datetime.utcnow() + timedelta(minutes=study_duration)
    
    db_reminder = Reminder(
        user_id=current_user.id,
        title="Take a Break!",
        message=f"You've been studying for {study_duration} minutes. Time for a 5-10 minute break!",
        reminder_type="break",
        scheduled_time=break_time
    )
    
    db.add(db_reminder)
    db.commit()
    
    return {"message": "Break reminder created", "break_time": break_time}

@router.post("/smart-recommendations")
async def create_smart_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create AI-powered smart reminder recommendations based on user patterns"""
    
    from app.services.ai_service import ai_service
    
    # Get user's progress records for analysis
    from app.models.database import ProgressRecord
    recent_progress = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id
    ).order_by(ProgressRecord.date.desc()).limit(10).all()
    
    if not recent_progress:
        return {"message": "No study history available for smart recommendations"}
    
    # Analyze patterns and create recommendations
    recommendations = analyze_study_patterns(recent_progress, current_user)
    
    created_reminders = []
    for rec in recommendations:
        db_reminder = Reminder(
            user_id=current_user.id,
            title=rec["title"],
            message=rec["message"],
            reminder_type="custom",
            scheduled_time=rec["scheduled_time"],
            is_recurring=rec.get("is_recurring", False),
            recurrence_pattern=rec.get("recurrence_pattern")
        )
        
        db.add(db_reminder)
        created_reminders.append(rec)
    
    db.commit()
    
    return {
        "message": f"Created {len(created_reminders)} smart reminders",
        "reminders": created_reminders
    }

@router.get("/upcoming")
async def get_upcoming_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    hours: int = 24
):
    """Get reminders coming up in the next specified hours"""
    
    end_time = datetime.utcnow() + timedelta(hours=hours)
    
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.scheduled_time > datetime.utcnow(),
        Reminder.scheduled_time <= end_time,
        Reminder.is_sent == False
    ).order_by(Reminder.scheduled_time.asc()).all()
    
    return [
        {
            "id": r.id,
            "title": r.title,
            "message": r.message,
            "scheduled_time": r.scheduled_time,
            "time_until": str(r.scheduled_time - datetime.utcnow()).split('.')[0]
        }
        for r in reminders
    ]

# Helper functions
def analyze_study_patterns(progress_records, user) -> List[dict]:
    """Analyze user study patterns and generate smart reminder recommendations"""
    recommendations = []
    
    if not progress_records:
        return recommendations
    
    # Find most productive study times
    study_hours = [record.date.hour for record in progress_records]
    if study_hours:
        most_common_hour = max(set(study_hours), key=study_hours.count)
        
        # Recommend daily study reminder at most productive time
        tomorrow_study_time = datetime.now().replace(
            hour=most_common_hour, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        
        recommendations.append({
            "title": "Daily Study Time",
            "message": f"Time for your daily study session! You're most productive at {most_common_hour}:00.",
            "scheduled_time": tomorrow_study_time,
            "is_recurring": True,
            "recurrence_pattern": "daily"
        })
    
    # Find subjects that need review
    subject_last_studied = {}
    for record in progress_records:
        if record.subject not in subject_last_studied:
            subject_last_studied[record.subject] = record.date
        else:
            if record.date > subject_last_studied[record.subject]:
                subject_last_studied[record.subject] = record.date
    
    # Create review reminders for subjects not studied recently
    for subject, last_date in subject_last_studied.items():
        days_ago = (datetime.utcnow() - last_date).days
        if days_ago > 3:  # Haven't studied this subject in 3 days
            review_time = datetime.utcnow() + timedelta(hours=2)
            recommendations.append({
                "title": f"Review {subject}",
                "message": f"It's been {days_ago} days since you studied {subject}. Time for a review session!",
                "scheduled_time": review_time
            })
    
    return recommendations

async def schedule_reminder_notification(reminder_id: int):
    """Background task to handle reminder notifications"""
    # In production, this would integrate with email/push notification services
    # For now, just mark as sent when the time comes
    import asyncio
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if reminder:
            # Calculate delay until scheduled time
            delay = (reminder.scheduled_time - datetime.utcnow()).total_seconds()
            if delay > 0:
                await asyncio.sleep(delay)
            
            # Mark as sent (in production, send actual notification here)
            reminder.is_sent = True
            db.commit()
            
            # Handle recurring reminders
            if reminder.is_recurring:
                create_next_recurring_reminder(reminder, db)
                
    finally:
        db.close()

def create_next_recurring_reminder(original_reminder: Reminder, db: Session):
    """Create the next occurrence of a recurring reminder"""
    if original_reminder.recurrence_pattern == "daily":
        next_time = original_reminder.scheduled_time + timedelta(days=1)
    elif original_reminder.recurrence_pattern == "weekly":
        next_time = original_reminder.scheduled_time + timedelta(weeks=1)
    elif original_reminder.recurrence_pattern == "monthly":
        next_time = original_reminder.scheduled_time + timedelta(days=30)
    else:
        return
    
    next_reminder = Reminder(
        user_id=original_reminder.user_id,
        title=original_reminder.title,
        message=original_reminder.message,
        reminder_type=original_reminder.reminder_type,
        scheduled_time=next_time,
        is_recurring=True,
        recurrence_pattern=original_reminder.recurrence_pattern
    )
    
    db.add(next_reminder)
    db.commit()