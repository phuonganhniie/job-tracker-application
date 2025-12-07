"""
Analytics schemas for response validation
"""
from pydantic import BaseModel
from typing import Dict, List


class StatusStatistics(BaseModel):
    """Statistics by status"""
    status: str
    count: int
    percentage: float


class SourceStatistics(BaseModel):
    """Statistics by source"""
    source: str
    total_applications: int
    hired_count: int
    rejected_count: int
    in_progress_count: int
    success_rate: float


class TimelineStatistics(BaseModel):
    """Timeline statistics"""
    period: str  # e.g., "2025-01", "Week 1"
    applications: int
    interviews: int
    offers: int
    hired: int


class AnalyticsSummary(BaseModel):
    """Overall analytics summary"""
    total_applications: int
    active_applications: int
    total_interviews: int
    upcoming_interviews: int
    offers_received: int
    hired_count: int
    rejected_count: int
    average_response_time_days: float
    success_rate: float


class AnalyticsResponse(BaseModel):
    """Complete analytics response"""
    summary: AnalyticsSummary
    by_status: List[StatusStatistics]
    by_source: List[SourceStatistics]
    timeline: List[TimelineStatistics]
