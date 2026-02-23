"""
Database Models for StudyWiseAI
SQLAlchemy models for all entities
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Profile information
    learning_style = Column(String)  # visual, auditory, kinesthetic
    study_goals = Column(Text)
    timezone = Column(String, default="UTC")
    
    # Relationships
    study_plans = relationship("StudyPlan", back_populates="user")
    study_sessions = relationship("StudySession", back_populates="user")
    progress_records = relationship("ProgressRecord", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
    career_sessions = relationship("CareerCounselingSession", back_populates="user")

class StudyPlan(Base):
    """AI-generated personalized study plans"""
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    subject = Column(String, nullable=False)
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    estimated_duration = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # AI-generated content
    study_materials = Column(JSON)  # List of topics/resources
    schedule = Column(JSON)  # Weekly schedule
    milestones = Column(JSON)  # Learning milestones
    
    # Relationships
    user = relationship("User", back_populates="study_plans")
    study_sessions = relationship("StudySession", back_populates="study_plan")

class StudySession(Base):
    """Individual study sessions"""
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    study_plan_id = Column(Integer, ForeignKey("study_plans.id"))
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    actual_duration = Column(Integer)  # actual time spent
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="planned")  # planned, active, completed, paused
    
    # Session data
    focus_score = Column(Float)  # 1-10 scale
    completion_rate = Column(Float)  # percentage
    notes = Column(Text)
    topics_covered = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    study_plan = relationship("StudyPlan", back_populates="study_sessions")

class ProgressRecord(Base):
    """Track user learning progress"""
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    subject = Column(String)
    topic = Column(String)
    
    # Progress metrics
    time_spent = Column(Integer)  # minutes
    sessions_completed = Column(Integer)
    accuracy_score = Column(Float)  # percentage
    retention_score = Column(Float)  # AI-calculated retention
    difficulty_level = Column(String)
    
    # AI insights
    learning_patterns = Column(JSON)
    recommendations = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")

class Reminder(Base):
    """Smart reminders and notifications"""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text)
    reminder_type = Column(String)  # study_session, break, review, custom
    scheduled_time = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String)  # daily, weekly, monthly
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reminders")

class ChatMessage(Base):
    """AI Assistant chat messages"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text)
    message_type = Column(String, default="question")  # question, study_help, general
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # AI context
    context_data = Column(JSON)  # Relevant user data for AI context
    confidence_score = Column(Float)  # AI response confidence
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")

class CareerCounselingSession(Base):
    """Career counseling sessions with AI"""
    __tablename__ = "career_counseling_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_profession = Column(String, nullable=False)
    session_status = Column(String, default="active")  # active, completed, paused
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Session data
    initial_questions = Column(Text)  # AI-generated initial questions
    user_responses = Column(Text)  # User's answers to questions
    action_plan = Column(Text)  # Generated career action plan
    session_notes = Column(Text)  # Additional notes or feedback
    
    # Relationships
    user = relationship("User", back_populates="career_sessions")

class LearningResource(Base):
    """Study materials and resources"""
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    resource_type = Column(String)  # article, video, quiz, flashcards
    subject = Column(String)
    difficulty_level = Column(String)
    url = Column(String)
    content = Column(Text)  # For text-based resources
    tags = Column(JSON)  # Searchable tags
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)