"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_db
from backend.services.analytics_service import AnalyticsService
from backend.schemas.analytics import AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Get complete analytics report including:
    - Summary statistics
    - Statistics by status
    - Statistics by source
    - Timeline data
    """
    analytics = AnalyticsService.get_complete_analytics(db)
    return analytics


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Get summary statistics only"""
    return AnalyticsService.get_summary_statistics(db)


@router.get("/by-status")
def get_by_status(db: Session = Depends(get_db)):
    """Get statistics grouped by status"""
    return AnalyticsService.get_statistics_by_status(db)


@router.get("/by-source")
def get_by_source(db: Session = Depends(get_db)):
    """Get statistics grouped by source"""
    return AnalyticsService.get_statistics_by_source(db)


@router.get("/timeline")
def get_timeline(
    period: str = "month",
    db: Session = Depends(get_db)
):
    """
    Get timeline statistics
    period: 'week', 'month', 'quarter'
    """
    return AnalyticsService.get_timeline_statistics(db, period)
