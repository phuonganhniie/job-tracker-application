"""
Interview service - API calls for interview operations
"""
from typing import Dict, List, Optional
from datetime import datetime
from frontend.services.api_client import APIClient


class InterviewService:
    """Service for interview-related API calls"""
    
    def __init__(self):
        self.client = APIClient()
    
    def create_interview(self, interview_data: Dict) -> Dict:
        """Create a new interview"""
        return self.client.post("/interviews/", interview_data)
    
    def get_interviews(self, filters: Optional[Dict] = None) -> Dict:
        """Get interviews with optional filters"""
        params = filters or {}
        return self.client.get("/interviews/", params=params)
    
    def get_interview_by_id(self, interview_id: int) -> Dict:
        """Get interview by ID"""
        return self.client.get(f"/interviews/{interview_id}")
    
    def get_interviews_by_job(self, job_id: int) -> Dict:
        """Get all interviews for a specific job"""
        return self.client.get(f"/interviews/job/{job_id}")
    
    def get_upcoming_interviews(self, days: int = 7) -> Dict:
        """Get upcoming interviews within specified days"""
        return self.client.get("/interviews/upcoming", params={"days": days})
    
    def get_interview_stats(self, job_id: Optional[int] = None) -> Dict:
        """Get interview statistics"""
        params = {}
        if job_id:
            params["job_id"] = job_id
        return self.client.get("/interviews/stats", params=params)
    
    def update_interview(self, interview_id: int, interview_data: Dict) -> Dict:
        """Update interview"""
        return self.client.put(f"/interviews/{interview_id}", interview_data)
    
    def update_interview_result(
        self, 
        interview_id: int, 
        result: str, 
        feedback: Optional[str] = None
    ) -> Dict:
        """Update interview result and feedback"""
        params = {"result": result}
        if feedback:
            params["feedback"] = feedback
        return self.client.patch(f"/interviews/{interview_id}/result", params=params)
    
    def delete_interview(self, interview_id: int) -> bool:
        """Delete interview"""
        try:
            self.client.delete(f"/interviews/{interview_id}")
            return True
        except Exception:
            return False


# Create singleton instance
interview_service = InterviewService()
