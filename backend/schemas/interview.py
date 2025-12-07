"""
Interview schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class InterviewBase(BaseModel):
    """Base interview schema"""
    job_id: int
    round_number: int = Field(..., ge=1)
    interview_type: Optional[str] = None
    scheduled_date: datetime
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    interviewer_name: Optional[str] = None
    interviewer_title: Optional[str] = None
    preparation_notes: Optional[str] = None
    feedback: Optional[str] = None
    result: Optional[str] = None


class InterviewCreate(InterviewBase):
    """Schema for creating an interview"""
    pass


class InterviewUpdate(BaseModel):
    """Schema for updating an interview (all fields optional)"""
    round_number: Optional[int] = None
    interview_type: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    interviewer_name: Optional[str] = None
    interviewer_title: Optional[str] = None
    preparation_notes: Optional[str] = None
    feedback: Optional[str] = None
    result: Optional[str] = None


class InterviewResponse(InterviewBase):
    """Schema for interview response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class InterviewListResponse(BaseModel):
    """Schema for interview list"""
    items: list[InterviewResponse]
    total: int


class InterviewFilter(BaseModel):
    """Schema for interview filtering"""
    job_id: Optional[int] = None
    interview_type: Optional[str] = None
    result: Optional[str] = None
    scheduled_date_from: Optional[datetime] = None
    scheduled_date_to: Optional[datetime] = None
