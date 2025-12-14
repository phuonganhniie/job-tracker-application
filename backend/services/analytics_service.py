"""
Analytics service - Business logic for analytics and reports
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Dict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from backend.models.job import Job
from backend.models.application import Application
from backend.models.interview import Interview
from backend.utils.constants import JobStatus, PIPELINE_ORDER
from backend.core.database import engine


def format_date_to_period(date_column):
    """
    Format date column to 'YYYY-MM' period string.
    Works with both SQLite and PostgreSQL.
    """
    db_type = engine.dialect.name
    
    if db_type == 'postgresql':
        # PostgreSQL: to_char(date, 'YYYY-MM')
        return func.to_char(date_column, 'YYYY-MM')
    else:
        # SQLite: strftime('%Y-%m', date)
        return func.strftime('%Y-%m', date_column)


class AnalyticsService:
    
    @staticmethod
    def get_summary_statistics(db: Session) -> Dict:
        """Get overall summary statistics - OPTIMIZED: 9 queries → 2 queries"""
        
        active_statuses = [JobStatus.APPLIED, JobStatus.SCREENING, JobStatus.INTERVIEW, JobStatus.OFFER]
        now = datetime.now()
        
        job_stats = db.query(
            func.count(Job.id).label('total'),
            func.sum(case((Job.current_status.in_([s.value for s in active_statuses]), 1), else_=0)).label('active'),
            func.sum(case((Job.current_status == JobStatus.OFFER.value, 1), else_=0)).label('offers'),
            func.sum(case((Job.current_status == JobStatus.HIRED.value, 1), else_=0)).label('hired'),
            func.sum(case((Job.current_status == JobStatus.REJECTED.value, 1), else_=0)).label('rejected')
        ).first()
        
        interview_stats = db.query(
            func.count(Interview.id).label('total'),
            func.sum(case((Interview.scheduled_date >= now, 1), else_=0)).label('upcoming')
        ).first()
        
        total_applications = getattr(job_stats, 'total', 0) or 0
        active_applications = getattr(job_stats, 'active', 0) or 0
        offers_received = getattr(job_stats, 'offers', 0) or 0
        hired_count = getattr(job_stats, 'hired', 0) or 0
        rejected_count = getattr(job_stats, 'rejected', 0) or 0
        total_interviews = getattr(interview_stats, 'total', 0) or 0
        upcoming_interviews = getattr(interview_stats, 'upcoming', 0) or 0
        
        success_rate = 0.0
        if (hired_count + rejected_count) > 0:
            success_rate = (hired_count / (hired_count + rejected_count)) * 100
        
        return {
            "total_applications": total_applications,
            "active_applications": active_applications,
            "total_interviews": total_interviews,
            "upcoming_interviews": upcoming_interviews,
            "offers_received": offers_received,
            "hired_count": hired_count,
            "rejected_count": rejected_count,
            "average_response_time_days": 7.5,
            "success_rate": round(success_rate, 2)
        }
    
    @staticmethod
    def get_statistics_by_status(db: Session) -> List[Dict]:
        
        total = db.query(func.count(Job.id)).scalar() or 1
        
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
        """Get timeline statistics - OPTIMIZED: 30 queries → 2 queries"""
        
        now = datetime.now()
        statistics = []
        
        for i in range(5, -1, -1):
            month_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) 
                          - relativedelta(months=i))
            month_end = month_start + relativedelta(months=1)
            
            statistics.append({
                "period": month_start.strftime("%Y-%m"),
                "month_start": month_start,
                "month_end": month_end,
                "month_start_date": month_start.date(),
                "month_end_date": month_end.date()
            })
        
        job_timeline = db.query(
            format_date_to_period(Job.applied_date).label('period'),
            func.count(Job.id).label('applications'),
            func.sum(case((Job.current_status == JobStatus.REJECTED.value, 1), else_=0)).label('rejected'),
            func.sum(case((Job.current_status == JobStatus.OFFER.value, 1), else_=0)).label('offers'),
            func.sum(case((Job.current_status == JobStatus.HIRED.value, 1), else_=0)).label('hired')
        ).filter(
            Job.applied_date >= statistics[0]['month_start_date']
        ).group_by(format_date_to_period(Job.applied_date)).all()
        
        interview_timeline = db.query(
            format_date_to_period(Interview.scheduled_date).label('period'),
            func.count(Interview.id).label('interviews')
        ).filter(
            Interview.scheduled_date >= statistics[0]['month_start']
        ).group_by(format_date_to_period(Interview.scheduled_date)).all()
        
        job_dict = {getattr(row, 'period', ''): row for row in job_timeline}
        interview_dict = {getattr(row, 'period', ''): row for row in interview_timeline}
        
        for stat in statistics:
            period = stat['period']
            job_data = job_dict.get(period)
            interview_data = interview_dict.get(period)
            
            stat['applications'] = getattr(job_data, 'applications', 0) if job_data else 0
            stat['interviews'] = getattr(interview_data, 'interviews', 0) if interview_data else 0
            stat['offers'] = getattr(job_data, 'offers', 0) if job_data else 0
            stat['hired'] = getattr(job_data, 'hired', 0) if job_data else 0
            stat['rejected'] = getattr(job_data, 'rejected', 0) if job_data else 0
            
            del stat['month_start']
            del stat['month_end']
            del stat['month_start_date']
            del stat['month_end_date']
        
        return statistics
    
    @staticmethod
    def get_complete_analytics(db: Session) -> Dict:
        
        return {
            "summary": AnalyticsService.get_summary_statistics(db),
            "by_status": AnalyticsService.get_statistics_by_status(db),
            "by_source": AnalyticsService.get_statistics_by_source(db),
            "timeline": AnalyticsService.get_timeline_statistics(db)
        }
