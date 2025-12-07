"""
Database initialization script
Run this to create the database tables
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.core.database import init_db, engine
from backend.models.job import Job
from backend.models.application import Application
from backend.models.interview import Interview
from backend.models.note import Note
from backend.models.email_template import EmailTemplate


def main():
    """Initialize database"""
    print("Initializing database...")
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
        print(f"📍 Database location: {engine.url}")
        
        # Print created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Created tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
