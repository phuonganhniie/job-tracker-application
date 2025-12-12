"""
Interview service - Business logic for interview operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from backend.models.interview import Interview
from backend.models.job import Job
from backend.schemas.interview import InterviewCreate, InterviewUpdate, InterviewFilter


class InterviewService:
    """Service class for interview operations"""
    
    @staticmethod
    def create_interview(db: Session, interview_data: InterviewCreate) -> Interview:
        """
        Create a new interview
        Validates that job_id exists
        """
        # Validate job exists
        job = db.query(Job).filter(Job.id == interview_data.job_id).first()
        if not job:
            raise ValueError(f"Job with id {interview_data.job_id} not found")
        
        # Create interview
        interview = Interview(**interview_data.model_dump())
        db.add(interview)
        db.commit()
        db.refresh(interview)
        
        return interview
    
    @staticmethod
    def get_interview_by_id(db: Session, interview_id: int) -> Optional[Interview]:
        """Get interview by ID"""
        return db.query(Interview).filter(Interview.id == interview_id).first()
    
    @staticmethod
    def get_interviews(
        db: Session,
        filters: Optional[InterviewFilter] = None
    ) -> tuple[List[Interview], int]:
        """
        Get interviews with optional filtering
        Returns (interviews, total_count)
        """
        query = db.query(Interview)
        
        if filters:
            # Filter by job_id
            if filters.job_id:
                query = query.filter(Interview.job_id == filters.job_id)
            
            # Filter by interview_type
            if filters.interview_type:
                query = query.filter(Interview.interview_type == filters.interview_type)
            
            # Filter by result
            if filters.result:
                query = query.filter(Interview.result == filters.result)
            
            # Filter by date range
            if filters.scheduled_date_from:
                query = query.filter(Interview.scheduled_date >= filters.scheduled_date_from)
            
            if filters.scheduled_date_to:
                query = query.filter(Interview.scheduled_date <= filters.scheduled_date_to)
        
        # Get total count
        total = query.count()
        
        # Order by scheduled_date descending (upcoming first)
        interviews = query.order_by(Interview.scheduled_date.desc()).all()
        
        return interviews, total
    
    @staticmethod
    def get_interviews_by_job(db: Session, job_id: int) -> List[Interview]:
        """Get all interviews for a specific job"""
        return db.query(Interview)\
            .filter(Interview.job_id == job_id)\
            .order_by(Interview.round_number.asc())\
            .all()
    
    @staticmethod
    def get_upcoming_interviews(
        db: Session, 
        days: int = 7
    ) -> List[Interview]:
        """Get upcoming interviews within specified days"""
        from datetime import timedelta
        
        now = datetime.now()
        end_date = now + timedelta(days=days)
        
        return db.query(Interview)\
            .filter(
                and_(
                    Interview.scheduled_date >= now,
                    Interview.scheduled_date <= end_date
                )
            )\
            .order_by(Interview.scheduled_date.asc())\
            .all()
    
    @staticmethod
    def update_interview(
        db: Session, 
        interview_id: int, 
        interview_data: InterviewUpdate
    ) -> Optional[Interview]:
        """Update interview"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return None
        
        # Update fields (only those provided)
        update_data = interview_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(interview, field, value)
        
        db.commit()
        db.refresh(interview)
        return interview
    
    @staticmethod
    def update_interview_result(
        db: Session,
        interview_id: int,
        result: str,
        feedback: Optional[str] = None
    ) -> Optional[Interview]:
        """
        Update interview result and feedback
        result should be: Passed, Failed, or Pending
        """
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return None
        
        interview.result = result
        if feedback:
            interview.feedback = feedback
        
        db.commit()
        db.refresh(interview)
        return interview
    
    @staticmethod
    def delete_interview(db: Session, interview_id: int) -> bool:
        """Delete interview"""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return False
        
        db.delete(interview)
        db.commit()
        return True
    
    @staticmethod
    def get_interview_stats(db: Session, job_id: Optional[int] = None) -> dict:
        """
        Get interview statistics
        If job_id provided, stats for that job only
        """
        query = db.query(Interview)
        
        if job_id:
            query = query.filter(Interview.job_id == job_id)
        
        interviews = query.all()
        
        total = len(interviews)
        passed = sum(1 for i in interviews if i.result == "Passed")
        failed = sum(1 for i in interviews if i.result == "Failed")
        pending = sum(1 for i in interviews if i.result == "Pending" or i.result is None)
        
        # Count by type
        by_type = {}
        for interview in interviews:
            itype = interview.interview_type or "Other"
            by_type[itype] = by_type.get(itype, 0) + 1
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pending": pending,
            "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
            "by_type": by_type
        }
