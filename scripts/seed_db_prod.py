#!/usr/bin/env python3
"""
Seed production database with sample data
Run this AFTER deploying to populate the database
"""
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
import random

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.core.database import SessionLocal, engine
from backend.models.job import Job
from backend.models.interview import Interview
from backend.models.note import Note
from backend.models.email_template import EmailTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clear_existing_data(db):
    """Clear existing data (optional, use with caution)"""
    try:
        db.query(Interview).delete()
        db.query(Note).delete()
        db.query(Job).delete()
        db.query(EmailTemplate).delete()
        db.commit()
        logger.info("✅ Cleared existing data")
    except Exception as e:
        logger.warning(f"⚠️ Could not clear data: {e}")
        db.rollback()


def seed_jobs(db):
    """Seed sample jobs"""
    logger.info("📝 Seeding jobs...")
    
    jobs_data = [
        # Applied
        {
            "company": "FPT Software", "title": "Senior Python Backend Developer", 
            "location": "Hà Nội", "source": "LinkedIn", "work_type": "Hybrid", 
            "current_status": "Applied", "days_ago": 3,
            "salary_min": 25000000, "salary_max": 40000000,
        },
        {
            "company": "VNG Corporation", "title": "Backend Engineer (Python/Go)", 
            "location": "TP.HCM", "source": "TopCV", "work_type": "Hybrid", 
            "current_status": "Applied", "days_ago": 5,
            "salary_min": 30000000, "salary_max": 50000000,
        },
        {
            "company": "Tiki", "title": "Full Stack Developer (Python/React)", 
            "location": "TP.HCM", "source": "VietnamWorks", "work_type": "Onsite", 
            "current_status": "Applied", "days_ago": 7,
            "salary_min": 20000000, "salary_max": 35000000,
        },
        # Screening
        {
            "company": "TMA Solutions", "title": "Python Backend Developer", 
            "location": "TP.HCM", "source": "LinkedIn", "work_type": "Hybrid", 
            "current_status": "Screening", "days_ago": 28,
            "salary_min": 20000000, "salary_max": 35000000,
        },
        {
            "company": "NashTech", "title": "Senior Software Engineer (Python)", 
            "location": "Đà Nẵng", "source": "Indeed", "work_type": "Remote", 
            "current_status": "Screening", "days_ago": 25,
            "salary_min": 25000000, "salary_max": 42000000,
        },
        # Interview
        {
            "company": "Grab Vietnam", "title": "Senior Backend Engineer", 
            "location": "TP.HCM", "source": "LinkedIn", "work_type": "Hybrid", 
            "current_status": "Interview", "days_ago": 35,
            "salary_min": 35000000, "salary_max": 60000000,
        },
        {
            "company": "Momo", "title": "Python Developer (Payment)", 
            "location": "TP.HCM", "source": "VietnamWorks", "work_type": "Hybrid", 
            "current_status": "Interview", "days_ago": 32,
            "salary_min": 28000000, "salary_max": 48000000,
        },
        # Offer
        {
            "company": "Sendo", "title": "Senior Python Developer", 
            "location": "TP.HCM", "source": "ITviec", "work_type": "Hybrid", 
            "current_status": "Offer", "days_ago": 45,
            "salary_min": 32000000, "salary_max": 52000000,
        },
        # Hired
        {
            "company": "Got It", "title": "Backend Engineer (AI Platform)", 
            "location": "Hà Nội", "source": "LinkedIn", "work_type": "Remote", 
            "current_status": "Hired", "days_ago": 60,
            "salary_min": 30000000, "salary_max": 50000000,
        },
        # Rejected
        {
            "company": "Lazada Vietnam", "title": "Senior Backend Developer", 
            "location": "TP.HCM", "source": "LinkedIn", "work_type": "Hybrid", 
            "current_status": "Rejected", "days_ago": 50,
            "salary_min": 32000000, "salary_max": 55000000,
        },
    ]
    
    jobs = []
    for job_data in jobs_data:
        days_ago = job_data.pop("days_ago", 0)
        applied_date = date.today() - timedelta(days=days_ago)
        
        job = Job(
            **job_data,
            applied_date=applied_date,
            job_url=f"https://example.com/jobs/{job_data['company'].lower().replace(' ', '-')}",
            job_description=f"Join {job_data['company']} as {job_data['title']}. Great opportunity!",
            priority="Medium"
        )
        jobs.append(job)
    
    db.add_all(jobs)
    db.commit()
    logger.info(f"✅ Created {len(jobs)} jobs")
    return jobs


def seed_interviews(db, jobs):
    """Seed sample interviews"""
    logger.info("📝 Seeding interviews...")
    
    # Get jobs in Interview status
    interview_jobs = [j for j in jobs if j.current_status == "Interview"]
    
    if not interview_jobs:
        logger.info("⚠️ No jobs in Interview status, skipping interviews")
        return
    
    interviews = []
    for job in interview_jobs[:2]:  # Add interviews for first 2 jobs
        interview = Interview(
            job_id=job.id,
            interview_type="Technical Interview",
            scheduled_date=datetime.now() + timedelta(days=random.randint(3, 10)),
            duration_minutes=60,
            location="Online",
            status="Scheduled",
            notes=f"Technical interview for {job.title} at {job.company}"
        )
        interviews.append(interview)
    
    db.add_all(interviews)
    db.commit()
    logger.info(f"✅ Created {len(interviews)} interviews")


def seed_email_templates(db):
    """Seed email templates"""
    logger.info("📝 Seeding email templates...")
    
    templates = [
        EmailTemplate(
            name="Thank You Email",
            subject="Thank you for the interview opportunity",
            body_template="Dear {recruiter_name},\n\nThank you for taking the time to interview me for the {job_title} position...",
            category="follow_up"
        ),
        EmailTemplate(
            name="Application Follow-up",
            subject="Following up on my application for {job_title}",
            body_template="Dear Hiring Manager,\n\nI wanted to follow up on my application for the {job_title} position...",
            category="follow_up"
        ),
    ]
    
    db.add_all(templates)
    db.commit()
    logger.info(f"✅ Created {len(templates)} email templates")


def main():
    """Main seed function"""
    try:
        logger.info("🚀 Starting database seeding...")
        logger.info(f"📊 Database: {engine.url}")
        
        db = SessionLocal()
        
        # Optional: Clear existing data (comment out if you want to keep existing data)
        # clear_existing_data(db)
        
        # Seed data
        jobs = seed_jobs(db)
        seed_interviews(db, jobs)
        seed_email_templates(db)
        
        db.close()
        
        logger.info("✅ Database seeded successfully!")
        logger.info("📊 Check your application to see the data")
        
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
