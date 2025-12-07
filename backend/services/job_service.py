"""
Job service - Business logic for job operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from datetime import date
from backend.models.job import Job
from backend.models.application import Application
from backend.schemas.job import JobCreate, JobUpdate, JobFilter
from backend.utils.constants import JobStatus


class JobService:
    """Service class for job operations"""
    
    @staticmethod
    def create_job(db: Session, job_data: JobCreate) -> Job:
        """
        Create a new job and add initial application status
        """
        # Create job
        job = Job(**job_data.model_dump())
        db.add(job)
        db.flush()  # Get job.id without committing
        
        # Create initial application record
        initial_application = Application(
            job_id=job.id,
            status=job.current_status,
            notes="Initial application submitted",
            status_date=job.applied_date
        )
        db.add(initial_application)
        db.commit()
        db.refresh(job)
        
        return job
    
    @staticmethod
    def get_job_by_id(db: Session, job_id: int) -> Optional[Job]:
        """Get job by ID"""
        return db.query(Job).filter(Job.id == job_id).first()
    
    @staticmethod
    def get_jobs(
        db: Session,
        filters: JobFilter
    ) -> tuple[List[Job], int]:
        """
        Get jobs with filtering, sorting, and pagination
        Returns (jobs, total_count)
        """
        query = db.query(Job)
        
        # Apply filters
        if filters.company_name:
            query = query.filter(Job.company_name.ilike(f"%{filters.company_name}%"))
        
        if filters.job_title:
            query = query.filter(Job.job_title.ilike(f"%{filters.job_title}%"))
        
        if filters.status:
            query = query.filter(Job.current_status == filters.status)
        
        if filters.source:
            query = query.filter(Job.source == filters.source)
        
        if filters.location:
            query = query.filter(Job.location.ilike(f"%{filters.location}%"))
        
        if filters.work_type:
            query = query.filter(Job.work_type == filters.work_type)
        
        if filters.is_favorite is not None:
            query = query.filter(Job.is_favorite == filters.is_favorite)
        
        if filters.applied_date_from:
            query = query.filter(Job.applied_date >= filters.applied_date_from)
        
        if filters.applied_date_to:
            query = query.filter(Job.applied_date <= filters.applied_date_to)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(Job, filters.sort_by, Job.applied_date)
        if filters.sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        offset = (filters.page - 1) * filters.page_size
        jobs = query.offset(offset).limit(filters.page_size).all()
        
        return jobs, total
    
    @staticmethod
    def update_job(db: Session, job_id: int, job_data: JobUpdate) -> Optional[Job]:
        """Update job"""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        
        # Update fields
        update_data = job_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def update_job_status(
        db: Session,
        job_id: int,
        new_status: str,
        notes: Optional[str] = None
    ) -> Optional[Job]:
        """
        Update job status and create application history record
        """
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        
        # Update job status
        job.current_status = new_status
        
        # Create application history record
        from datetime import datetime
        application = Application(
            job_id=job_id,
            status=new_status,
            notes=notes,
            status_date=datetime.now()
        )
        db.add(application)
        
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def delete_job(db: Session, job_id: int) -> bool:
        """Delete job (cascade deletes applications, interviews, notes)"""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return False
        
        db.delete(job)
        db.commit()
        return True
    
    @staticmethod
    def search_jobs(db: Session, keyword: str, limit: int = 20) -> List[Job]:
        """
        Search jobs by keyword (company name or job title)
        """
        return db.query(Job).filter(
            or_(
                Job.company_name.ilike(f"%{keyword}%"),
                Job.job_title.ilike(f"%{keyword}%")
            )
        ).limit(limit).all()
