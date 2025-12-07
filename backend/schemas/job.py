"""
Job schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# Base schema with common fields
class JobBase(BaseModel):
    """Base job schema"""
    company_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    location: Optional[str] = None
    work_type: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_currency: str = "VND"
    source: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    current_status: str = "Applied"
    applied_date: date
    deadline: Optional[date] = None
    is_favorite: bool = False


# Schema for creating a new job
class JobCreate(JobBase):
    """Schema for creating a job"""
    pass


# Schema for updating a job
class JobUpdate(BaseModel):
    """Schema for updating a job (all fields optional)"""
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    location: Optional[str] = None
    work_type: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_currency: Optional[str] = None
    source: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    current_status: Optional[str] = None
    applied_date: Optional[date] = None
    deadline: Optional[date] = None
    is_favorite: Optional[bool] = None


# Schema for job response
class JobResponse(JobBase):
    """Schema for job response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schema for job list with pagination
class JobListResponse(BaseModel):
    """Schema for paginated job list"""
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Schema for job search/filter
class JobFilter(BaseModel):
    """Schema for job filtering"""
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    location: Optional[str] = None
    work_type: Optional[str] = None
    is_favorite: Optional[bool] = None
    applied_date_from: Optional[date] = None
    applied_date_to: Optional[date] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str = "applied_date"
    sort_order: str = "desc"  # asc or desc
