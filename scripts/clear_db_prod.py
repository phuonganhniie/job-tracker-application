"""
Script to clear all data from production database (for re-seeding)
"""
import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.database import SessionLocal, engine
from backend.models.job import Job
from backend.models.interview import Interview
from backend.models.note import Note
from backend.models.application import Application
from backend.models.email_template import EmailTemplate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clear_all_data():
    """Clear all data from database (respecting foreign key constraints)"""
    logger.info("🗑️  Starting database cleanup...")
    logger.info(f"📊 Database: {engine.url}")
    
    try:
        db = SessionLocal()
        
        # Delete in reverse order of dependencies
        logger.info("Deleting notes...")
        db.query(Note).delete()
        
        logger.info("Deleting applications...")
        db.query(Application).delete()
        
        logger.info("Deleting interviews...")
        db.query(Interview).delete()
        
        logger.info("Deleting email templates...")
        db.query(EmailTemplate).delete()
        
        logger.info("Deleting jobs...")
        db.query(Job).delete()
        
        db.commit()
        db.close()
        
        logger.info("✅ Database cleared successfully!")
        logger.info("💡 Restart your backend service to trigger auto-seed")
        
    except Exception as e:
        logger.error(f"❌ Clear failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Safety confirmation
    confirm = input("⚠️  This will DELETE ALL DATA from the database. Type 'YES' to confirm: ")
    if confirm == "YES":
        clear_all_data()
    else:
        logger.info("❌ Operation cancelled")
