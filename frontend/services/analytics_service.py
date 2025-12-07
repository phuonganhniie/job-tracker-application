"""
Analytics service - API calls for analytics
"""
from typing import Dict
from frontend.services.api_client import APIClient


class AnalyticsService:
    """Service for analytics-related API calls"""
    
    def __init__(self):
        self.client = APIClient()
    
    def get_analytics(self) -> Dict:
        """Get complete analytics report"""
        return self.client.get("/analytics/")
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return self.client.get("/analytics/summary")
    
    def get_by_status(self) -> Dict:
        """Get statistics by status"""
        return self.client.get("/analytics/by-status")
    
    def get_by_source(self) -> Dict:
        """Get statistics by source"""
        return self.client.get("/analytics/by-source")
    
    def get_timeline(self, period: str = "month") -> Dict:
        """Get timeline statistics"""
        return self.client.get("/analytics/timeline", params={"period": period})


# Create singleton instance
analytics_service = AnalyticsService()
