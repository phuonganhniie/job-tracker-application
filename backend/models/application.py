"""
Application model - Pipeline status history
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Application(Base):
    """Application status history model"""
    __tablename__ = "applications"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Status Information
    status = Column(String(50), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    status_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(id={self.id}, job_id={self.job_id}, status='{self.status}', date={self.status_date})>"
