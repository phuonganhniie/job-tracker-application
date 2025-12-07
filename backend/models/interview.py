"""
Interview model - Interview schedule and details
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Interview(Base):
    """Interview schedule model"""
    __tablename__ = "interviews"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Interview Information
    round_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.
    interview_type = Column(String(50), nullable=True)  # Phone, Video, Onsite, Technical
    scheduled_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Location/Meeting
    location = Column(String(255), nullable=True)  # Physical location
    meeting_link = Column(Text, nullable=True)  # Online meeting link
    
    # Interviewer Information
    interviewer_name = Column(String(255), nullable=True)
    interviewer_title = Column(String(255), nullable=True)
    
    # Notes & Results
    preparation_notes = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    result = Column(String(50), nullable=True)  # Passed/Failed/Pending
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="interviews")
    notes = relationship("Note", back_populates="interview", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Interview(id={self.id}, job_id={self.job_id}, round={self.round_number}, date={self.scheduled_date})>"
