"""
Frontend settings
"""
import os

# API Configuration
# Support environment variable for production deployment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
API_URL = f"{API_BASE_URL}{API_V1_PREFIX}"

# Pagination
DEFAULT_PAGE_SIZE = 20

# Status colors
STATUS_COLORS = {
    "Applied": "🔵",
    "Screening": "🟡",
    "Interview": "🟠",
    "Offer": "🟢",
    "Hired": "✅",
    "Rejected": "❌",
    "Withdrawn": "⚪"
}

# Interview type icons
INTERVIEW_TYPE_ICONS = {
    "Phone Screening": "📞",
    "Video Call": "💻",
    "Technical Test": "⚙️",
    "Onsite Interview": "🏢",
    "Final Round": "🎯",
    "HR Interview": "👔"
}

# Priority colors
PRIORITY_COLORS = {
    "Low": "info",
    "Medium": "warning",
    "High": "error"
}
