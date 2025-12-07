"""
Base API client
"""
import requests
from typing import Dict, Any, Optional
from frontend.config.settings import API_URL


class APIClient:
    """Base API client for making HTTP requests"""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.timeout = 30
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get("detail", str(e)) if response.text else str(e)
            raise Exception(f"API Error: {error_detail}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data, timeout=self.timeout)
        return self._handle_response(response)
    
    def patch(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """PATCH request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, timeout=self.timeout)
        return self._handle_response(response)
