"""
Job API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.api.deps import get_db
from backend.services.job_service import JobService
from backend.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse,
    JobFilter
)
import math

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    job = JobService.create_job(db, job_data)
    return job


@router.get("/", response_model=JobListResponse)
def get_jobs(
    company_name: str = None,
    job_title: str = None,
    status: str = None,
    source: str = None,
    location: str = None,
    work_type: str = None,
    is_favorite: bool = None,
    applied_date_from: str = None,
    applied_date_to: str = None,
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "applied_date",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Get jobs with filtering, sorting, and pagination
    """
    # Convert string dates to date objects if provided
    from datetime import datetime
    date_from = datetime.fromisoformat(applied_date_from).date() if applied_date_from else None
    date_to = datetime.fromisoformat(applied_date_to).date() if applied_date_to else None
    
    filters = JobFilter(
        company_name=company_name,
        job_title=job_title,
        status=status,
        source=source,
        location=location,
        work_type=work_type,
        is_favorite=is_favorite,
        applied_date_from=date_from,
        applied_date_to=date_to,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    jobs, total = JobService.get_jobs(db, filters)
    
    return JobListResponse(
        items=jobs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get job by ID"""
    job = JobService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):
    """Update job"""
    job = JobService.update_job(db, job_id, job_data)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.patch("/{job_id}/status", response_model=JobResponse)
def update_job_status(
    job_id: int,
    new_status: str,
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Update job status and create application history"""
    job = JobService.update_job_status(db, job_id, new_status, notes)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Delete job"""
    success = JobService.delete_job(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return None


@router.get("/search/{keyword}", response_model=List[JobResponse])
def search_jobs(
    keyword: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search jobs by keyword"""
    jobs = JobService.search_jobs(db, keyword, limit)
    return jobs
