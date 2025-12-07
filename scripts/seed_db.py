"""
Seed database with sample data
"""
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
import random

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.core.database import SessionLocal
from backend.models.job import Job
from backend.models.application import Application
from backend.models.interview import Interview
from backend.models.note import Note
from backend.models.email_template import EmailTemplate


def seed_jobs(db):
    """Seed sample jobs"""
    companies = [
        ("FPT Software", "Python Developer", "LinkedIn", "Remote"),
        ("VNG Corporation", "Backend Engineer", "TopCV", "Hybrid"),
        ("Viettel Digital", "Full Stack Developer", "VietnamWorks", "Onsite"),
        ("TMA Solutions", "Software Engineer", "LinkedIn", "Hybrid"),
        ("NashTech", "Python Developer", "Indeed", "Remote"),
    ]
    
    statuses = ["Applied", "Screening", "Interview", "Offer", "Hired"]
    
    jobs = []
    for idx, (company, title, source, work_type) in enumerate(companies):
        applied_date = date.today() - timedelta(days=random.randint(1, 60))
        
        job = Job(
            company_name=company,
            job_title=title,
            location="Hà Nội" if idx % 2 == 0 else "TP.HCM",
            work_type=work_type,
            salary_min=15000000 + idx * 2000000,
            salary_max=25000000 + idx * 3000000,
            salary_currency="VND",
            source=source,
            current_status=statuses[idx % len(statuses)],
            applied_date=applied_date,
            is_favorite=idx % 2 == 0
        )
        db.add(job)
        jobs.append(job)
    
    db.commit()
    print(f"✅ Created {len(jobs)} sample jobs")
    return jobs


def seed_applications(db, jobs):
    """Seed application history"""
    for job in jobs:
        # Initial application
        app = Application(
            job_id=job.id,
            status="Applied",
            notes="Đã nộp hồ sơ qua " + job.source,
            status_date=job.applied_date
        )
        db.add(app)
    
    db.commit()
    print(f"✅ Created application history")


def seed_interviews(db, jobs):
    """Seed sample interviews"""
    interview_types = ["Phone Screening", "Technical Test", "Final Round"]
    
    count = 0
    for job in jobs[:3]:  # Add interviews for first 3 jobs
        scheduled = datetime.now() + timedelta(days=random.randint(1, 14))
        
        interview = Interview(
            job_id=job.id,
            round_number=1,
            interview_type=random.choice(interview_types),
            scheduled_date=scheduled,
            meeting_link="https://meet.google.com/abc-xyz",
            interviewer_name="Mr. Nguyễn Văn A",
            result="Pending"
        )
        db.add(interview)
        count += 1
    
    db.commit()
    print(f"✅ Created {count} sample interviews")


def seed_email_templates(db):
    """Seed email templates"""
    templates = [
        {
            "template_name": "Thank You Email",
            "template_type": "Thank_You",
            "subject": "Thank you for the interview - {job_title} position",
            "body": "Dear {interviewer_name},\n\nThank you for taking the time to interview me for the {job_title} position at {company_name}...",
            "variables": '{"company_name": "Company name", "job_title": "Job title", "interviewer_name": "Interviewer name"}'
        },
        {
            "template_name": "Follow Up Email",
            "template_type": "Follow_Up",
            "subject": "Following up on {job_title} application",
            "body": "Dear Hiring Manager,\n\nI wanted to follow up on my application for the {job_title} position...",
            "variables": '{"company_name": "Company name", "job_title": "Job title"}'
        }
    ]
    
    for t in templates:
        template = EmailTemplate(**t)
        db.add(template)
    
    db.commit()
    print(f"✅ Created {len(templates)} email templates")


def main():
    """Seed database"""
    print("Seeding database with sample data...")
    
    db = SessionLocal()
    try:
        jobs = seed_jobs(db)
        seed_applications(db, jobs)
        seed_interviews(db, jobs)
        seed_email_templates(db)
        
        print("\n🎉 Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
