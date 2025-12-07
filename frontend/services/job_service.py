"""
Job service - API calls for job operations
"""
from typing import Dict, List, Optional
from frontend.services.api_client import APIClient


class JobService:
    """Service for job-related API calls"""
    
    def __init__(self):
        self.client = APIClient()
    
    def create_job(self, job_data: Dict) -> Dict:
        """Create a new job"""
        return self.client.post("/jobs/", job_data)
    
    def get_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict] = None
    ) -> Dict:
        """Get jobs with pagination and filters"""
        params = {
            "page": page,
            "page_size": page_size
        }
        if filters:
            params.update(filters)
        
        return self.client.get("/jobs/", params=params)
    
    def get_job_by_id(self, job_id: int) -> Dict:
        """Get job by ID"""
        return self.client.get(f"/jobs/{job_id}")
    
    def update_job(self, job_id: int, job_data: Dict) -> Dict:
        """Update job"""
        return self.client.put(f"/jobs/{job_id}", job_data)
    
    def update_job_status(self, job_id: int, new_status: str, notes: Optional[str] = None) -> Dict:
        """Update job status"""
        params = {"new_status": new_status}
        if notes:
            params["notes"] = notes
        return self.client.patch(f"/jobs/{job_id}/status", params=params)
    
    def delete_job(self, job_id: int) -> Dict:
        """Delete job"""
        return self.client.delete(f"/jobs/{job_id}")
    
    def search_jobs(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Search jobs by keyword"""
        return self.client.get(f"/jobs/search/{keyword}", params={"limit": limit})


# Create singleton instance
job_service = JobService()
