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
    """Seed realistic production jobs - Student graduation project data"""
    logger.info("📝 Seeding production jobs...")
    
    jobs_data = [
        # ACTIVE APPLICATIONS (Đang theo dõi)
        {
            "company_name": "VNG Corporation", 
            "job_title": "Backend Engineer (Python)", 
            "location": "TP. Hồ Chí Minh", 
            "source": "LinkedIn", 
            "work_type": "Hybrid", 
            "current_status": "Interview", 
            "days_ago": 15,
            "salary_min": 25000000, 
            "salary_max": 40000000,
            "url": "https://tuyendung.vng.com.vn/careers/backend-engineer-python",
            "description": "Phát triển backend services cho Zalo ecosystem. Stack: Python, FastAPI, PostgreSQL, Redis, Docker. Team size 8-10 người, Agile methodology.",
            "contact_person": "Ms. Nguyễn Thu Hà",
            "contact_email": "ha.nguyen@vng.com.vn",
            "contact_phone": "028-3939-0888"
        },
        {
            "company_name": "Tiki", 
            "job_title": "Python Backend Developer", 
            "location": "TP. Hồ Chí Minh", 
            "source": "TopCV", 
            "work_type": "Hybrid", 
            "current_status": "Screening", 
            "days_ago": 8,
            "salary_min": 20000000, 
            "salary_max": 35000000,
            "url": "https://tuyendung.tiki.vn/job/python-backend-developer",
            "description": "Join Tiki Seller Platform team. Requirements: 2+ years Python, FastAPI/Django, MySQL. Build features cho seller dashboard và inventory management.",
            "contact_person": "Mr. Trần Minh Quân",
            "contact_email": "quan.tran@tiki.vn",
            "contact_phone": "028-6268-8883"
        },
        {
            "company_name": "FPT Software", 
            "job_title": "Junior Backend Developer", 
            "location": "Hà Nội", 
            "source": "VietnamWorks", 
            "work_type": "Onsite", 
            "current_status": "Applied", 
            "days_ago": 5,
            "salary_min": 12000000, 
            "salary_max": 18000000,
            "url": "https://fptsoftware.com/careers/junior-backend-developer",
            "description": "Fresher/Junior position cho Finance project. Outsourcing cho client Nhật Bản. Training included, good for new graduates.",
            "contact_person": "Ms. Lê Thị Mai",
            "contact_email": "mai.le@fpt.com.vn"
        },
        
        # POSITIVE OUTCOMES (Kết quả tích cực)
        {
            "company_name": "Shopee Vietnam", 
            "job_title": "Backend Engineer Intern", 
            "location": "TP. Hồ Chí Minh", 
            "source": "ITviec", 
            "work_type": "Onsite", 
            "current_status": "Offer", 
            "days_ago": 35,
            "salary_min": 8000000, 
            "salary_max": 12000000,
            "url": "https://careers.shopee.vn/jobs/backend-engineer-intern",
            "description": "6-month internship program. Làm việc với Payment team. Convert to full-time possibility. Offer received: 10M/month + laptop + insurance.",
            "contact_person": "Mr. Phạm Đức Anh",
            "contact_email": "anh.pham@shopee.com",
            "contact_phone": "028-7300-9200",
            "notes": "Offer expires: 2025-12-20. Need to respond by then."
        },
        {
            "company_name": "Momo", 
            "job_title": "Software Engineer (Backend)", 
            "location": "TP. Hồ Chí Minh", 
            "source": "LinkedIn", 
            "work_type": "Hybrid", 
            "current_status": "Offer", 
            "days_ago": 42,
            "salary_min": 15000000, 
            "salary_max": 25000000,
            "url": "https://momo.vn/careers/software-engineer-backend",
            "description": "Fintech product team. Python, FastAPI, PostgreSQL, Kafka. Great benefits package. Offer: 18M gross + 13th month + performance bonus.",
            "contact_person": "Ms. Hoàng Thị Linh",
            "contact_email": "linh.hoang@momo.vn",
            "notes": "Best offer so far. Considering between Momo and Shopee."
        },
        
        # PAST APPLICATIONS (Lưu trữ)
        {
            "company_name": "Base.vn", 
            "job_title": "Python Developer", 
            "location": "Hà Nội", 
            "source": "TopCV", 
            "work_type": "Remote", 
            "current_status": "Rejected", 
            "days_ago": 60,
            "salary_min": 15000000, 
            "salary_max": 25000000,
            "url": "https://base.vn/tuyen-dung/python-developer",
            "description": "E-commerce platform. Remote work. Rejected after technical test - need to improve algorithm skills.",
            "notes": "Feedback: Good Python knowledge but weak on data structures & algorithms. Should practice more on LeetCode."
        },
        {
            "company_name": "KiotViet", 
            "job_title": "Backend Developer", 
            "location": "TP. Hồ Chí Minh", 
            "source": "CareerBuilder", 
            "work_type": "Hybrid", 
            "current_status": "Withdrawn", 
            "days_ago": 50,
            "salary_min": 12000000, 
            "salary_max": 20000000,
            "url": "https://www.kiotviet.vn/tuyen-dung/backend-developer",
            "description": "Retail management software. Withdrew application after receiving better offers.",
            "notes": "Withdrew on 2025-11-05 to focus on Shopee and Momo opportunities."
        },
    ]
    
    jobs = []
    for job_data in jobs_data:
        days_ago = job_data.pop("days_ago", 0)
        applied_date = date.today() - timedelta(days=days_ago)
        
        # Extract and map fields correctly
        url = job_data.pop("url", None)
        description = job_data.pop("description", None)
        notes_text = job_data.pop("notes", None)  # Will be added later
        contact_person = job_data.pop("contact_person", None)
        contact_email = job_data.pop("contact_email", None)
        contact_phone = job_data.pop("contact_phone", None)
        
        job = Job(
            **job_data,
            applied_date=applied_date,
            job_url=url,
            job_description=description,
            contact_person=contact_person,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        jobs.append(job)
    
    db.add_all(jobs)
    db.commit()
    
    # Refresh all jobs to get their IDs
    for job in jobs:
        db.refresh(job)
    
    logger.info(f"✅ Created {len(jobs)} production jobs")
    return jobs


def seed_interviews(db, jobs):
    """Seed realistic production interviews"""
    logger.info("📝 Seeding production interviews...")
    
    # Find specific jobs for interviews
    vng_job = next((j for j in jobs if j.company_name == "VNG Corporation"), None)
    
    if not vng_job:
        logger.info("⚠️ No jobs found for interviews, skipping")
        return []
    
    interviews_data = [
        {
            "job_id": vng_job.id,
            "round_number": 2,
            "interview_type": "Technical Interview",
            "scheduled_date": datetime.now() + timedelta(days=3),
            "location": "VNG Campus, Tòa Z.06, Đường số 13, Tân Thuận Đông, Quận 7, TP.HCM",
            "interviewer_name": "Mr. Nguyễn Văn Hoàng",
            "interviewer_title": "Tech Lead",
            "preparation_notes": "Round 2/3 - Technical deep dive. Topics: Python advanced, System Design, Database optimization. Prepare: FastAPI project demo, explain architecture decisions.",
            "result": "Pending"
        },
        {
            "job_id": vng_job.id,
            "round_number": 1,
            "interview_type": "Phone Screening", 
            "scheduled_date": datetime.now() - timedelta(days=7),
            "location": "Phone Call",
            "interviewer_name": "Ms. Nguyễn Thu Hà",
            "interviewer_title": "HR Manager",
            "feedback": "Round 1/3 - Passed. Discussed background, motivation, salary expectation. Next: Technical interview with team lead.",
            "result": "Passed"
        },
    ]
    
    interviews = []
    for interview_data in interviews_data:
        interview = Interview(**interview_data)
        interviews.append(interview)
    
    db.add_all(interviews)
    db.commit()
    
    # Refresh to get IDs
    for interview in interviews:
        db.refresh(interview)
    
    logger.info(f"✅ Created {len(interviews)} production interviews")
    return interviews


def seed_notes(db, jobs, interviews):
    """Seed production notes"""
    logger.info("📝 Seeding production notes...")
    
    # Find specific jobs
    shopee_job = next((j for j in jobs if j.company_name == "Shopee Vietnam"), None)
    momo_job = next((j for j in jobs if j.company_name == "Momo"), None)
    base_job = next((j for j in jobs if j.company_name == "Base.vn"), None)
    
    notes = []
    
    # Job notes
    if shopee_job:
        notes.append(Note(
            job_id=shopee_job.id,
            note_type="decision",
            title="Offer Decision Deadline",
            content="Offer expires: 2025-12-20. Need to respond by then. Considering: Good for internship experience, but lower salary compared to Momo full-time offer.",
            priority="High"
        ))
    
    if momo_job:
        notes.append(Note(
            job_id=momo_job.id,
            note_type="decision",
            title="Best Offer - Final Decision",
            content="Best offer so far: 18M gross + 13th month + performance bonus. Fintech product team. Great for career growth. Considering between Momo (full-time) and Shopee (internship).",
            priority="High"
        ))
    
    if base_job:
        notes.append(Note(
            job_id=base_job.id,
            note_type="feedback",
            title="Rejection Feedback",
            content="Feedback from technical test: Good Python knowledge but weak on data structures & algorithms. Should practice more on LeetCode before applying to similar positions.",
            priority="Medium"
        ))
    
    # Interview notes
    if interviews and len(interviews) > 0:
        notes.append(Note(
            interview_id=interviews[0].id,
            note_type="preparation",
            title="Technical Interview Preparation",
            content="Topics to review: 1) FastAPI advanced features 2) System Design principles 3) Database optimization techniques 4) Docker & deployment. Prepare demo project to showcase.",
            priority="High"
        ))
    
    db.add_all(notes)
    db.commit()
    logger.info(f"✅ Created {len(notes)} production notes")
    return notes


def seed_applications(db, jobs):
    """Seed application status history"""
    logger.info("📝 Seeding application history...")
    
    from backend.models.application import Application
    
    # Find VNG job to add status history
    vng_job = next((j for j in jobs if j.company_name == "VNG Corporation"), None)
    
    if not vng_job:
        logger.info("⚠️ No jobs found for applications, skipping")
        return []
    
    applications = [
        Application(
            job_id=vng_job.id,
            status="Applied",
            status_date=datetime.now() - timedelta(days=15),
            notes="Submitted application via LinkedIn. Resume reviewed and customized for backend role."
        ),
        Application(
            job_id=vng_job.id,
            status="Screening",
            status_date=datetime.now() - timedelta(days=10),
            notes="HR reached out for phone screening. Discussed background, salary expectations."
        ),
        Application(
            job_id=vng_job.id,
            status="Interview",
            status_date=datetime.now() - timedelta(days=7),
            notes="Passed phone screening. Scheduled for technical interview next week."
        ),
    ]
    
    db.add_all(applications)
    db.commit()
    logger.info(f"✅ Created {len(applications)} application history records")
    return applications


def seed_email_templates(db):
    """Seed production-ready email templates"""
    logger.info("📝 Seeding email templates...")
    
    templates = [
        EmailTemplate(
            name="Thank You After Interview",
            subject="Thank you for the interview - {job_title} position",
            body_template="""Dear {interviewer_name},

Thank you for taking the time to interview me for the {job_title} position at {company} on {interview_date}.

I enjoyed learning more about the role and the team. The discussion about {specific_topic} was particularly interesting, and I'm excited about the possibility of contributing to {project_name}.

I believe my experience with {relevant_skills} aligns well with the team's needs, and I'm eager to bring value to {company}.

Please let me know if you need any additional information. I look forward to hearing from you.

Best regards,
{your_name}""",
            category="follow_up"
        ),
        EmailTemplate(
            name="Application Status Follow-up",
            subject="Following up on {job_title} application",
            body_template="""Dear {recruiter_name},

I hope this email finds you well.

I applied for the {job_title} position at {company} on {applied_date}, and I wanted to follow up on the status of my application.

I remain very interested in this opportunity and believe my skills in {key_skills} would be a great fit for your team.

Would it be possible to get an update on the timeline for next steps?

Thank you for your time and consideration.

Best regards,
{your_name}
{your_email}
{your_phone}""",
            category="follow_up"
        ),
        EmailTemplate(
            name="Offer Acceptance",
            subject="Acceptance of {job_title} Offer",
            body_template="""Dear {recruiter_name},

I am delighted to formally accept the offer for the {job_title} position at {company}.

I confirm the following details:
- Position: {job_title}
- Start Date: {start_date}
- Salary: {salary_amount}
- Benefits: {benefits_summary}

I appreciate the opportunity and look forward to contributing to the team. Please let me know the next steps and any documents you need from me.

Thank you once again for this opportunity.

Best regards,
{your_name}""",
            category="acceptance"
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
        
        # Seed data in correct order (respect foreign key constraints)
        jobs = seed_jobs(db)
        interviews = seed_interviews(db, jobs)
        seed_notes(db, jobs, interviews)
        seed_applications(db, jobs)
        seed_email_templates(db)
        
        db.close()
        
        logger.info("✅ Database seeded successfully!")
        logger.info("📊 Summary:")
        logger.info(f"  - Jobs: {len(jobs)}")
        logger.info(f"  - Interviews: {len(interviews)}")
        logger.info(f"  - Email Templates: 3")
        logger.info("📊 Check your application to see the data")
        
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
