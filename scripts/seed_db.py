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
    """Seed sample jobs with rich data"""
    companies_data = [
        # Tech Companies - Applied status
        ("FPT Software", "Senior Python Developer", "LinkedIn", "Remote", "Applied", 30),
        ("VNG Corporation", "Backend Engineer (Python/FastAPI)", "TopCV", "Hybrid", "Applied", 25),
        ("Tiki", "Full Stack Developer", "VietnamWorks", "Onsite", "Applied", 20),
        ("Shopee Vietnam", "Software Engineer", "CareerBuilder", "Hybrid", "Applied", 15),
        
        # Screening stage
        ("TMA Solutions", "Python Backend Developer", "LinkedIn", "Hybrid", "Screening", 28),
        ("NashTech", "Senior Software Engineer", "Indeed", "Remote", "Screening", 22),
        ("Viettel Digital", "Full Stack Developer", "TopCV", "Onsite", "Screening", 18),
        
        # Interview stage
        ("Grab Vietnam", "Backend Engineer", "LinkedIn", "Hybrid", "Interview", 35),
        ("Momo", "Python Developer", "VietnamWorks", "Hybrid", "Interview", 32),
        ("VinID", "Software Engineer", "TopCV", "Onsite", "Interview", 26),
        
        # Offer stage
        ("FPT IS", "Senior Python Developer", "LinkedIn", "Remote", "Offer", 40),
        ("KMS Technology", "Backend Developer", "TopCV", "Hybrid", "Offer", 38),
        
        # Hired
        ("NashTech", "Python Developer", "Indeed", "Remote", "Hired", 45),
        
        # Rejected
        ("Google Vietnam", "Software Engineer", "LinkedIn", "Hybrid", "Rejected", 50),
        ("Amazon Vietnam", "Backend Engineer", "LinkedIn", "Remote", "Rejected", 48),
        ("Meta Vietnam", "Full Stack Developer", "LinkedIn", "Hybrid", "Rejected", 42),
        ("Microsoft Vietnam", "Software Developer", "LinkedIn", "Onsite", "Rejected", 38),
    ]
    
    locations = ["Hà Nội", "TP.HCM", "Đà Nẵng"]
    
    jobs = []
    for idx, (company, title, source, work_type, status, days_ago) in enumerate(companies_data):
        applied_date = date.today() - timedelta(days=days_ago)
        
        # Calculate deadline (usually 30-60 days after applied)
        if status not in ["Rejected", "Hired"]:
            deadline = applied_date + timedelta(days=random.randint(30, 60))
        else:
            deadline = None
        
        job = Job(
            company_name=company,
            job_title=title,
            location=random.choice(locations),
            work_type=work_type,
            salary_min=15000000 + idx * 1500000,
            salary_max=25000000 + idx * 2000000,
            salary_currency="VND",
            source=source,
            current_status=status,
            applied_date=applied_date,
            deadline=deadline,
            is_favorite=idx % 3 == 0,
            job_url=f"https://careers.{company.lower().replace(' ', '')}.com/jobs/{idx}",
            job_description=f"We are looking for a talented {title} to join our team..."
        )
        db.add(job)
        jobs.append(job)
    
    db.commit()
    print(f"✅ Created {len(jobs)} sample jobs with rich data")
    return jobs


def seed_applications(db, jobs):
    """Seed comprehensive application history"""
    for job in jobs:
        # Initial application
        app = Application(
            job_id=job.id,
            status="Applied",
            notes=f"Đã nộp hồ sơ qua {job.source}. CV và cover letter đã được gửi.",
            status_date=job.applied_date
        )
        db.add(app)
        
        # Add progression based on current status
        if job.current_status in ["Screening", "Interview", "Offer", "Hired", "Rejected"]:
            # Add screening status
            screening_date = job.applied_date + timedelta(days=random.randint(3, 7))
            app2 = Application(
                job_id=job.id,
                status="Screening",
                notes="Nhận được phản hồi từ HR. Hồ sơ đang được xem xét.",
                status_date=screening_date
            )
            db.add(app2)
        
        if job.current_status in ["Interview", "Offer", "Hired", "Rejected"]:
            # Add interview status
            interview_date = job.applied_date + timedelta(days=random.randint(10, 15))
            app3 = Application(
                job_id=job.id,
                status="Interview",
                notes="Đã hoàn thành vòng phỏng vấn kỹ thuật. Chờ kết quả.",
                status_date=interview_date
            )
            db.add(app3)
        
        if job.current_status in ["Offer", "Hired"]:
            # Add offer status
            offer_date = job.applied_date + timedelta(days=random.randint(20, 30))
            app4 = Application(
                job_id=job.id,
                status="Offer",
                notes="Nhận được offer! Đang review package và benefits.",
                status_date=offer_date
            )
            db.add(app4)
        
        if job.current_status == "Hired":
            # Add hired status
            hired_date = job.applied_date + timedelta(days=random.randint(35, 45))
            app5 = Application(
                job_id=job.id,
                status="Hired",
                notes="Đã chấp nhận offer và ký hợp đồng. Sẽ onboard vào tuần tới.",
                status_date=hired_date
            )
            db.add(app5)
        
        if job.current_status == "Rejected":
            # Add rejected status
            rejected_date = job.applied_date + timedelta(days=random.randint(5, 25))
            app_rejected = Application(
                job_id=job.id,
                status="Rejected",
                notes="Nhận thông báo không phù hợp. Có thể do kinh nghiệm chưa đủ hoặc không match với yêu cầu.",
                status_date=rejected_date
            )
            db.add(app_rejected)
    
    db.commit()
    print(f"✅ Created comprehensive application history")


def seed_interviews(db, jobs):
    """Seed comprehensive interview data"""
    interview_types = ["Phone Screening", "Technical Test", "Coding Challenge", "System Design", "HR Round", "Final Round"]
    interviewers = [
        "Mr. Nguyễn Văn A - Technical Lead",
        "Ms. Trần Thị B - Senior Developer",
        "Mr. Lê Văn C - Engineering Manager", 
        "Ms. Phạm Thị D - HR Manager",
        "Mr. Hoàng Văn E - CTO"
    ]
    
    results = ["Passed", "Pending", "Failed"]
    
    count = 0
    for job in jobs:
        # Add interviews for jobs in Interview, Offer, or Hired status
        if job.current_status in ["Interview", "Offer", "Hired"]:
            # Round 1: Phone Screening (always completed)
            interview1 = Interview(
                job_id=job.id,
                round_number=1,
                interview_type="Phone Screening",
                scheduled_date=job.applied_date + timedelta(days=random.randint(5, 10)),
                meeting_link="https://meet.google.com/abc-xyz-001",
                interviewer_name=random.choice(interviewers),
                result="Passed",
                feedback="Candidate shows good communication skills and relevant experience."
            )
            db.add(interview1)
            count += 1
            
            # Round 2: Technical Test
            interview2 = Interview(
                job_id=job.id,
                round_number=2,
                interview_type=random.choice(["Technical Test", "Coding Challenge"]),
                scheduled_date=job.applied_date + timedelta(days=random.randint(12, 18)),
                meeting_link="https://meet.google.com/abc-xyz-002",
                interviewer_name=random.choice(interviewers),
                result="Passed" if job.current_status in ["Offer", "Hired"] else random.choice(["Passed", "Pending"]),
                feedback="Strong technical skills demonstrated in coding challenge."
            )
            db.add(interview2)
            count += 1
            
            # Round 3: Final Round (only for Offer/Hired)
            if job.current_status in ["Offer", "Hired"]:
                interview3 = Interview(
                    job_id=job.id,
                    round_number=3,
                    interview_type="Final Round",
                    scheduled_date=job.applied_date + timedelta(days=random.randint(20, 28)),
                    meeting_link="https://meet.google.com/abc-xyz-003",
                    interviewer_name=random.choice(interviewers),
                    result="Passed",
                    feedback="Excellent culture fit. Team is excited to have them onboard."
                )
                db.add(interview3)
                count += 1
        
        # Add upcoming interviews for jobs in Screening status
        elif job.current_status == "Screening":
            scheduled = datetime.now() + timedelta(days=random.randint(3, 10))
            interview = Interview(
                job_id=job.id,
                round_number=1,
                interview_type="Phone Screening",
                scheduled_date=scheduled,
                meeting_link=f"https://meet.google.com/upcoming-{random.randint(100, 999)}",
                interviewer_name=random.choice(interviewers),
                result="Pending"
            )
            db.add(interview)
            count += 1
    
    db.commit()
    print(f"✅ Created {count} comprehensive interview records")


def seed_notes(db, jobs):
    """Seed notes for various jobs"""
    note_contents = [
        ("Research", "Company Research", "Company có văn hóa làm việc tốt, review trên Glassdoor khá cao (4.2/5). Tech stack: Python, FastAPI, PostgreSQL, Docker, K8s."),
        ("Preparation", "Interview Preparation", "Cần ôn lại kiến thức về: System Design, Database Optimization, Microservices Architecture."),
        ("Interview Prep", "Technical Questions", "Questions có thể hỏi: 1) Kinh nghiệm với FastAPI, 2) Xử lý concurrency, 3) Database indexing strategies."),
        ("Salary Negotiation", "Compensation Plan", "Mục tiêu: 25-30M VND gross. Benefits quan trọng: health insurance, remote flexibility, learning budget."),
        ("Follow Up", "Post-Interview Follow-up", "Đã gửi thank you email sau phỏng vấn. HR hẹn feedback trong vòng 3-5 ngày làm việc."),
        ("General", "Position Info", "Position này match tốt với career goals. Team size: 8-10 người, dự án: Fintech platform."),
    ]
    
    priorities = ["Low", "Medium", "High"]
    
    count = 0
    for job in jobs[:12]:  # Add notes for first 12 jobs
        # Add 1-3 notes per job
        num_notes = random.randint(1, 3)
        selected_notes = random.sample(note_contents, num_notes)
        
        for note_type, title, content in selected_notes:
            note = Note(
                job_id=job.id,
                note_type=note_type,
                title=title,
                content=content,
                priority=random.choice(priorities)
            )
            db.add(note)
            count += 1
    
    db.commit()
    print(f"✅ Created {count} comprehensive notes")


def seed_email_templates(db):
    """Seed email templates"""
    # Check if templates already exist
    existing = db.query(EmailTemplate).count()
    if existing > 0:
        print(f"⏭️  Email templates already exist ({existing} templates), skipping...")
        return
    
    templates = [
        {
            "template_name": "Thank You Email",
            "template_type": "Thank_You",
            "subject": "Thank you for the interview - {job_title} position",
            "body": """Dear {interviewer_name},

Thank you for taking the time to interview me for the {job_title} position at {company_name}. I really enjoyed our conversation and learning more about the role and your team.

I am very excited about the opportunity to contribute to {company_name} and believe my skills in Python development align well with your needs.

Please let me know if you need any additional information from me.

Looking forward to hearing from you.

Best regards,
[Your Name]""",
            "variables": '{"company_name": "Company name", "job_title": "Job title", "interviewer_name": "Interviewer name"}'
        },
        {
            "template_name": "Follow Up Email",
            "template_type": "Follow_Up",
            "subject": "Following up on {job_title} application",
            "body": """Dear Hiring Manager,

I wanted to follow up on my application for the {job_title} position at {company_name} that I submitted on {applied_date}.

I am very interested in this opportunity and would love to discuss how my experience in backend development can contribute to your team.

Would it be possible to schedule a brief call to discuss my application?

Thank you for your consideration.

Best regards,
[Your Name]""",
            "variables": '{"company_name": "Company name", "job_title": "Job title", "applied_date": "Application date"}'
        },
        {
            "template_name": "Salary Negotiation Email",
            "template_type": "Negotiation",
            "subject": "Regarding the offer for {job_title} position",
            "body": """Dear {hr_name},

Thank you for extending the offer for the {job_title} position at {company_name}. I am very excited about this opportunity.

After careful consideration, I would like to discuss the compensation package. Based on my experience and market research, I was hoping for a salary in the range of {expected_salary}.

I am confident that I can bring significant value to {company_name} and would love to find a mutually beneficial agreement.

Could we schedule a call to discuss this further?

Best regards,
[Your Name]""",
            "variables": '{"company_name": "Company name", "job_title": "Job title", "hr_name": "HR name", "expected_salary": "Expected salary"}'
        },
        {
            "template_name": "Offer Acceptance Email",
            "template_type": "Acceptance",
            "subject": "Acceptance of offer - {job_title} position",
            "body": """Dear {hr_name},

I am delighted to formally accept the offer for the {job_title} position at {company_name}.

I am excited to join the team and contribute to {company_name}'s success. As discussed, my start date will be {start_date}.

Please let me know the next steps for onboarding and any documents I need to prepare.

Thank you again for this wonderful opportunity.

Best regards,
[Your Name]""",
            "variables": '{"company_name": "Company name", "job_title": "Job title", "hr_name": "HR name", "start_date": "Start date"}'
        }
    ]
    
    for t in templates:
        template = EmailTemplate(**t)
        db.add(template)
    
    db.commit()
    print(f"✅ Created {len(templates)} email templates")


def main():
    """Seed database"""
    print("🌱 Seeding database with comprehensive sample data...")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        jobs = seed_jobs(db)
        seed_applications(db, jobs)
        seed_interviews(db, jobs)
        seed_notes(db, jobs)
        seed_email_templates(db)
        
        print("=" * 60)
        print("\n🎉 Database seeded successfully with rich data!")
        print(f"""
📊 Summary:
   - {len(jobs)} jobs across different stages
   - Full application history for each job
   - Multiple interview rounds
   - Detailed notes and templates
        """)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
