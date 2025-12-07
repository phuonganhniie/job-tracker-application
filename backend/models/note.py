"""
Note model - Notes for jobs and interviews
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Note(Base):
    """Note model for jobs and interviews"""
    __tablename__ = "notes"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys (at least one must be set)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Note Information
    note_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default="Medium")  # Low/Medium/High
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="notes")
    interview = relationship("Interview", back_populates="notes")
    
    def __repr__(self):
        return f"<Note(id={self.id}, type='{self.note_type}', title='{self.title}')>"
