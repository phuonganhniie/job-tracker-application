"""SQLAlchemy models"""

# Import all models to ensure relationships can be resolved
from backend.models.job import Job
from backend.models.application import Application
from backend.models.interview import Interview
from backend.models.note import Note
from backend.models.email_template import EmailTemplate

__all__ = ["Job", "Application", "Interview", "Note", "EmailTemplate"]
