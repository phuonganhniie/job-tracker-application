"""
EmailTemplate model - Email templates for various purposes
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.core.database import Base


class EmailTemplate(Base):
    """Email template model"""
    __tablename__ = "email_templates"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Template Information
    template_name = Column(String(255), nullable=False, unique=True, index=True)
    template_type = Column(String(50), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    
    # Variables (stored as JSON string)
    variables = Column(Text, nullable=True)  # JSON format: {"var1": "description", ...}
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<EmailTemplate(id={self.id}, name='{self.template_name}', type='{self.template_type}')>"
