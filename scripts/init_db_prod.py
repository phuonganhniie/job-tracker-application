#!/usr/bin/env python3
"""
Production database initialization script
Runs automatically on deployment to create tables
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.core.database import init_db, engine
from backend.models import job, interview, application, note, email_template  # noqa: F401
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Initialize database tables for production"""
    try:
        logger.info("🚀 Starting database initialization...")
        logger.info(f"📊 Database URL: {engine.url}")
        
        # Create all tables
        init_db()
        
        logger.info("✅ Database tables created successfully!")
        logger.info("📋 Tables: jobs, interviews, applications, notes, email_templates")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
