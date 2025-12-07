"""
Application schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ApplicationBase(BaseModel):
    """Base application schema"""
    job_id: int
    status: str = Field(..., min_length=1, max_length=50)
    notes: Optional[str] = None
    status_date: datetime


class ApplicationCreate(ApplicationBase):
    """Schema for creating an application status"""
    pass


class ApplicationUpdate(BaseModel):
    """Schema for updating an application"""
    status: Optional[str] = None
    notes: Optional[str] = None
    status_date: Optional[datetime] = None


class ApplicationResponse(ApplicationBase):
    """Schema for application response"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ApplicationListResponse(BaseModel):
    """Schema for application list"""
    items: list[ApplicationResponse]
    total: int
