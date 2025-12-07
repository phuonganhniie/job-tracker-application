"""
Job model - Main entity for job applications
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Job(Base):
    """Job application model"""
    __tablename__ = "jobs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Job Information
    company_name = Column(String(255), nullable=False, index=True)
    job_title = Column(String(255), nullable=False)
    job_url = Column(Text, nullable=True)
    job_description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    work_type = Column(String(50), nullable=True)  # Remote/Hybrid/Onsite
    
    # Salary Information
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    salary_currency = Column(String(10), default="VND")
    
    # Source & Contact
    source = Column(String(100), nullable=True, index=True)  # LinkedIn, Indeed, etc.
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    
    # Status & Dates
    current_status = Column(String(50), nullable=False, default="Applied", index=True)
    applied_date = Column(Date, nullable=False, index=True)
    deadline = Column(Date, nullable=True)
    
    # Metadata
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="job", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(id={self.id}, company='{self.company_name}', title='{self.job_title}', status='{self.current_status}')>"
