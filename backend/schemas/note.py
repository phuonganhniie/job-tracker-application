"""
Note schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    """Base note schema"""
    job_id: Optional[int] = None
    interview_id: Optional[int] = None
    note_type: str = Field(..., min_length=1, max_length=50)
    title: Optional[str] = None
    content: str = Field(..., min_length=1)
    priority: str = "Medium"
    
    @field_validator('job_id', 'interview_id')
    @classmethod
    def check_at_least_one_id(cls, v, info):
        """Ensure at least one of job_id or interview_id is provided"""
        if info.data.get('job_id') is None and info.data.get('interview_id') is None:
            raise ValueError('Either job_id or interview_id must be provided')
        return v


class NoteCreate(NoteBase):
    """Schema for creating a note"""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note"""
    note_type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None


class NoteResponse(NoteBase):
    """Schema for note response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NoteListResponse(BaseModel):
    """Schema for note list"""
    items: list[NoteResponse]
    total: int


class NoteFilter(BaseModel):
    """Schema for note filtering"""
    job_id: Optional[int] = None
    interview_id: Optional[int] = None
    note_type: Optional[str] = None
    priority: Optional[str] = None
