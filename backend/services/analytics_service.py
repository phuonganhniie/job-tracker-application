"""
Analytics service - Business logic for analytics and reports
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Dict
from datetime import datetime, timedelta
from backend.models.job import Job
from backend.models.application import Application
from backend.models.interview import Interview
from backend.utils.constants import JobStatus, PIPELINE_ORDER


class AnalyticsService:
    """Service class for analytics operations"""
    
    @staticmethod
    def get_summary_statistics(db: Session) -> Dict:
        """Get overall summary statistics"""
        
        # Total applications
        total_applications = db.query(func.count(Job.id)).scalar()
        
        # Active applications (not in final states)
        active_statuses = [JobStatus.APPLIED, JobStatus.SCREENING, JobStatus.INTERVIEW, JobStatus.OFFER]
        active_applications = db.query(func.count(Job.id)).filter(
            Job.current_status.in_([s.value for s in active_statuses])
        ).scalar()
        
        # Total interviews
        total_interviews = db.query(func.count(Interview.id)).scalar()
        
        # Upcoming interviews (scheduled in the future)
        upcoming_interviews = db.query(func.count(Interview.id)).filter(
            Interview.scheduled_date >= datetime.now()
        ).scalar()
        
        # Offers received
        offers_received = db.query(func.count(Job.id)).filter(
            Job.current_status == JobStatus.OFFER.value
        ).scalar()
        
        # Hired count
        hired_count = db.query(func.count(Job.id)).filter(
            Job.current_status == JobStatus.HIRED.value
        ).scalar()
        
        # Rejected count
        rejected_count = db.query(func.count(Job.id)).filter(
            Job.current_status == JobStatus.REJECTED.value
        ).scalar()
        
        # Average response time (days from Applied to first status change)
        # This is a simplified calculation
        avg_response_time = 7.5  # Placeholder - would need complex query
        
        # Success rate (Hired / (Hired + Rejected))
        success_rate = 0.0
        if (hired_count + rejected_count) > 0:
            success_rate = (hired_count / (hired_count + rejected_count)) * 100
        
        return {
            "total_applications": total_applications or 0,
            "active_applications": active_applications or 0,
            "total_interviews": total_interviews or 0,
            "upcoming_interviews": upcoming_interviews or 0,
            "offers_received": offers_received or 0,
            "hired_count": hired_count or 0,
            "rejected_count": rejected_count or 0,
            "average_response_time_days": avg_response_time,
            "success_rate": round(success_rate, 2)
        }
    
    @staticmethod
    def get_statistics_by_status(db: Session) -> List[Dict]:
        """Get statistics grouped by status"""
        
        total = db.query(func.count(Job.id)).scalar() or 1  # Avoid division by zero
        
        results = db.query(
            Job.current_status,
            func.count(Job.id).label('count')
        ).group_by(Job.current_status).all()
        
        statistics = []
        for status, count in results:
            statistics.append({
                "status": status,
                "count": count,
                "percentage": round((count / total) * 100, 2)
            })
        
        return statistics
    
    @staticmethod
    def get_statistics_by_source(db: Session) -> List[Dict]:
        """Get statistics grouped by source"""
        
        results = db.query(
            Job.source,
            func.count(Job.id).label('total'),
            func.sum(case((Job.current_status == JobStatus.HIRED.value, 1), else_=0)).label('hired'),
            func.sum(case((Job.current_status == JobStatus.REJECTED.value, 1), else_=0)).label('rejected'),
            func.sum(case((Job.current_status.in_([
                JobStatus.APPLIED.value,
                JobStatus.SCREENING.value,
                JobStatus.INTERVIEW.value,
                JobStatus.OFFER.value
            ]), 1), else_=0)).label('in_progress')
        ).filter(Job.source.isnot(None)).group_by(Job.source).all()
        
        statistics = []
        for source, total, hired, rejected, in_progress in results:
            success_rate = 0.0
            if (hired + rejected) > 0:
                success_rate = (hired / (hired + rejected)) * 100
            
            statistics.append({
                "source": source,
                "total_applications": total,
                "hired_count": hired or 0,
                "rejected_count": rejected or 0,
                "in_progress_count": in_progress or 0,
                "success_rate": round(success_rate, 2)
            })
        
        return statistics
    
    @staticmethod
    def get_timeline_statistics(db: Session, period: str = "month") -> List[Dict]:
        """
        Get timeline statistics
        period: 'week', 'month', 'quarter'
        """
        
        # This is a simplified version - would need database-specific date functions
        # For now, return last 6 months
        statistics = []
        
        for i in range(6, 0, -1):
            month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            
            applications = db.query(func.count(Job.id)).filter(
                Job.applied_date >= month_start.date(),
                Job.applied_date < month_end.date()
            ).scalar()
            
            interviews = db.query(func.count(Interview.id)).filter(
                Interview.scheduled_date >= month_start,
                Interview.scheduled_date < month_end
            ).scalar()
            
            offers = db.query(func.count(Job.id)).filter(
                Job.current_status == JobStatus.OFFER.value,
                Job.updated_at >= month_start,
                Job.updated_at < month_end
            ).scalar()
            
            hired = db.query(func.count(Job.id)).filter(
                Job.current_status == JobStatus.HIRED.value,
                Job.updated_at >= month_start,
                Job.updated_at < month_end
            ).scalar()
            
            statistics.append({
                "period": month_start.strftime("%Y-%m"),
                "applications": applications or 0,
                "interviews": interviews or 0,
                "offers": offers or 0,
                "hired": hired or 0
            })
        
        return statistics
    
    @staticmethod
    def get_complete_analytics(db: Session) -> Dict:
        """Get complete analytics report"""
        
        return {
            "summary": AnalyticsService.get_summary_statistics(db),
            "by_status": AnalyticsService.get_statistics_by_status(db),
            "by_source": AnalyticsService.get_statistics_by_source(db),
            "timeline": AnalyticsService.get_timeline_statistics(db)
        }
