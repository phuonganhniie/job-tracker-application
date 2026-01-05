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
    """Seed sample jobs with rich, realistic data"""
    companies_data = [
        # Applied (Mới nộp hồ sơ) - 8 jobs
        {
            "company": "FPT Software", "title": "Senior Python Backend Developer", "location": "Hà Nội",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Applied", "days_ago": 3,
            "salary_min": 25000000, "salary_max": 40000000,
            "url": "https://www.linkedin.com/jobs/view/senior-python-developer-fpt-123456",
            "contact": ("Nguyễn Thu Hương", "huong.nguyen@fpt.com.vn", "0912-345-678"),
            "description": "Tham gia phát triển hệ thống backend cho dự án Fintech lớn. Yêu cầu: 5+ năm kinh nghiệm Python, thành thạo FastAPI/Django, PostgreSQL, Redis, Docker."
        },
        {
            "company": "VNG Corporation", "title": "Backend Engineer (Python/Go)", "location": "TP.HCM",
            "source": "TopCV", "work_type": "Hybrid", "status": "Applied", "days_ago": 5,
            "salary_min": 30000000, "salary_max": 50000000,
            "url": "https://tuyendung.vng.com.vn/backend-engineer-python",
            "contact": ("Trần Minh Khoa", "khoa.tran@vng.com.vn", "0923-456-789"),
            "description": "Phát triển các services cho Zalo, ZaloPay. Tech stack: Python, Go, Microservices, Kafka, K8s. Làm việc với team quốc tế."
        },
        {
            "company": "Tiki", "title": "Full Stack Developer (Python/React)", "location": "TP.HCM",
            "source": "VietnamWorks", "work_type": "Onsite", "status": "Applied", "days_ago": 7,
            "salary_min": 20000000, "salary_max": 35000000,
            "url": "https://tuyendung.tiki.vn/fullstack-developer-2024",
            "contact": ("Lê Thị Mai", "mai.le@tiki.vn", "0934-567-890"),
            "description": "Xây dựng features mới cho Tiki Platform. Yêu cầu: Python, FastAPI, React, MySQL, Redis. Team năng động, sáng tạo."
        },
        {
            "company": "Shopee Vietnam", "title": "Software Engineer (Backend)", "location": "TP.HCM",
            "source": "CareerBuilder", "work_type": "Hybrid", "status": "Applied", "days_ago": 10,
            "salary_min": 28000000, "salary_max": 45000000,
            "url": "https://careers.shopee.vn/jobs/software-engineer-backend",
            "contact": ("Phạm Văn Long", "long.pham@shopee.com", "0945-678-901"),
            "description": "Phát triển hệ thống e-commerce quy mô lớn. Python, Django, MySQL, Redis, RabbitMQ. Cơ hội làm việc với tech team khu vực."
        },
        {
            "company": "Viettel Digital", "title": "Python Developer (AI/ML)", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Onsite", "status": "Applied", "days_ago": 12,
            "salary_min": 22000000, "salary_max": 38000000,
            "url": "https://viettelsolutions.vn/tuyen-dung/python-ai-ml",
            "contact": ("Ngô Thị Lan", "lan.ngo@viettel.com.vn", "0956-789-012"),
            "description": "Phát triển giải pháp AI/ML cho các dự án Telecom. Python, TensorFlow, PyTorch, FastAPI. Làm việc với data quy mô lớn."
        },
        {
            "company": "MISA JSC", "title": "Senior Backend Developer", "location": "Hà Nội",
            "source": "ITviec", "work_type": "Hybrid", "status": "Applied", "days_ago": 14,
            "salary_min": 20000000, "salary_max": 35000000,
            "url": "https://www.itviec.com/jobs/senior-backend-developer-misa",
            "contact": ("Hoàng Văn Tùng", "tung.hoang@misa.com.vn", "0967-890-123"),
            "description": "Phát triển phần mềm kế toán, quản lý doanh nghiệp. Python, Django, PostgreSQL, Docker. Môi trường product company."
        },
        {
            "company": "Be Group", "title": "Backend Engineer (Ride-hailing)", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Applied", "days_ago": 18,
            "salary_min": 24000000, "salary_max": 40000000,
            "url": "https://be.com.vn/careers/backend-engineer",
            "contact": ("Đỗ Thị Hồng", "hong.do@be.com.vn", "0978-901-234"),
            "description": "Xây dựng platform gọi xe công nghệ. Python, FastAPI, PostgreSQL, Redis, Kafka. Team trẻ, năng động."
        },
        {
            "company": "Base.vn", "title": "Python Developer (E-commerce)", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Remote", "status": "Applied", "days_ago": 21,
            "salary_min": 18000000, "salary_max": 30000000,
            "url": "https://base.vn/tuyen-dung/python-developer",
            "contact": ("Vũ Minh Tuấn", "tuan.vu@base.vn", "0989-012-345"),
            "description": "Phát triển nền tảng bán hàng omnichannel. Python, Django, MySQL, ElasticSearch. Làm việc remote 100%."
        },
        
        # Screening (Đang review hồ sơ) - 5 jobs
        {
            "company": "TMA Solutions", "title": "Python Backend Developer", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Screening", "days_ago": 28,
            "salary_min": 20000000, "salary_max": 35000000,
            "url": "https://www.tma.com.vn/careers/python-backend-dev",
            "contact": ("Nguyễn Thị Hoa", "hoa.nguyen@tma.com.vn", "0901-234-567"),
            "description": "Outsourcing cho khách hàng Nhật Bản. Python, Django, PostgreSQL. Cơ hội onsite Nhật."
        },
        {
            "company": "NashTech", "title": "Senior Software Engineer (Python)", "location": "Đà Nẵng",
            "source": "Indeed", "work_type": "Remote", "status": "Screening", "days_ago": 25,
            "salary_min": 25000000, "salary_max": 42000000,
            "url": "https://www.nashtechglobal.com/careers/senior-python",
            "contact": ("Trần Văn Nam", "nam.tran@nashtechglobal.com", "0912-345-678"),
            "description": "Dự án cho khách hàng UK. Python, FastAPI, AWS, Docker, K8s. Remote flexible."
        },
        {
            "company": "FPT IS", "title": "Tech Lead (Python/Microservices)", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Hybrid", "status": "Screening", "days_ago": 22,
            "salary_min": 35000000, "salary_max": 55000000,
            "url": "https://fptis.com.vn/tuyen-dung/tech-lead-python",
            "contact": ("Lê Văn Đức", "duc.le@fpt.com", "0923-456-789"),
            "description": "Dẫn dắt team 5-7 người. Kiến trúc microservices, Python, Go, K8s, AWS. Dự án Banking."
        },
        {
            "company": "KMS Technology", "title": "Backend Developer (Healthcare)", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Screening", "days_ago": 20,
            "salary_min": 24000000, "salary_max": 40000000,
            "url": "https://kms-technology.com/careers/backend-healthcare",
            "contact": ("Phạm Thị Linh", "linh.pham@kms-technology.com", "0934-567-890"),
            "description": "Phát triển giải pháp Healthcare cho thị trường US. Python, Django, PostgreSQL, AWS."
        },
        {
            "company": "CMC Global", "title": "Python Developer (Fintech)", "location": "Hà Nội",
            "source": "VietnamWorks", "work_type": "Onsite", "status": "Screening", "days_ago": 18,
            "salary_min": 22000000, "salary_max": 38000000,
            "url": "https://cmcglobal.com.vn/careers/python-fintech",
            "contact": ("Ngô Văn Hùng", "hung.ngo@cmcglobal.com.vn", "0945-678-901"),
            "description": "Xây dựng hệ thống thanh toán điện tử. Python, FastAPI, PostgreSQL, Redis, Celery."
        },
        
        # Interview (Đang phỏng vấn) - 4 jobs
        {
            "company": "Grab Vietnam", "title": "Senior Backend Engineer", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Interview", "days_ago": 35,
            "salary_min": 35000000, "salary_max": 60000000,
            "url": "https://grab.careers/senior-backend-engineer-hcm",
            "contact": ("Lê Thị Phương", "phuong.le@grab.com", "0956-789-012"),
            "description": "Build scalable systems cho Grab platform. Python, Go, Microservices, K8s, AWS. Competitive package."
        },
        {
            "company": "Momo", "title": "Python Developer (Payment)", "location": "TP.HCM",
            "source": "VietnamWorks", "work_type": "Hybrid", "status": "Interview", "days_ago": 32,
            "salary_min": 28000000, "salary_max": 48000000,
            "url": "https://momo.vn/tuyen-dung/python-payment",
            "contact": ("Trần Minh Quân", "quan.tran@momo.vn", "0967-890-123"),
            "description": "Phát triển hệ thống thanh toán ví điện tử. Python, FastAPI, MySQL, Redis, Kafka. Fast-paced environment."
        },
        {
            "company": "VinID", "title": "Software Engineer (Platform)", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Onsite", "status": "Interview", "days_ago": 28,
            "salary_min": 26000000, "salary_max": 45000000,
            "url": "https://vinid.net/tuyen-dung/software-engineer",
            "contact": ("Hoàng Thị Mai", "mai.hoang@vinid.net", "0978-901-234"),
            "description": "Xây dựng nền tảng loyalty & rewards. Python, Django, PostgreSQL, Redis. Benefits tốt."
        },
        {
            "company": "Techcombank", "title": "Backend Developer (Digital Banking)", "location": "Hà Nội",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Interview", "days_ago": 25,
            "salary_min": 30000000, "salary_max": 50000000,
            "url": "https://careers.techcombank.com.vn/backend-developer",
            "contact": ("Nguyễn Văn Thành", "thanh.nguyen@techcombank.com.vn", "0989-012-345"),
            "description": "Digital transformation cho ngân hàng. Python, Java, Microservices, Oracle, K8s. Bank benefits."
        },
        
        # Offer (Đã nhận offer) - 2 jobs
        {
            "company": "Sendo", "title": "Senior Python Developer", "location": "TP.HCM",
            "source": "ITviec", "work_type": "Hybrid", "status": "Offer", "days_ago": 45,
            "salary_min": 32000000, "salary_max": 52000000,
            "url": "https://sendo.vn/tuyen-dung/senior-python",
            "contact": ("Đặng Thị Hương", "huong.dang@sendo.vn", "0901-234-567"),
            "description": "Phát triển marketplace platform. Python, Django, MySQL, Redis, AWS. Offer: 45M + bonus + equity."
        },
        {
            "company": "VIB Bank", "title": "Python Backend Engineer", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Onsite", "status": "Offer", "days_ago": 42,
            "salary_min": 28000000, "salary_max": 46000000,
            "url": "https://www.vib.com.vn/careers/python-backend",
            "contact": ("Vũ Văn Hải", "hai.vu@vib.com.vn", "0912-345-678"),
            "description": "Core banking modernization. Python, FastAPI, Oracle, Redis. Offer: 40M + 13th month + insurance."
        },
        
        # Hired (Đã được tuyển) - 1 job
        {
            "company": "Got It", "title": "Backend Engineer (AI Platform)", "location": "Hà Nội",
            "source": "LinkedIn", "work_type": "Remote", "status": "Hired", "days_ago": 60,
            "salary_min": 30000000, "salary_max": 50000000,
            "url": "https://www.got-it.ai/careers/backend-engineer",
            "contact": ("Trần Thị Nga", "nga.tran@got-it.ai", "0923-456-789"),
            "description": "Build AI-powered platform. Python, FastAPI, PostgreSQL, Redis, AWS. Start date: 15/01/2025."
        },
        
        # Rejected (Bị từ chối) - 5 jobs
        {
            "company": "Lazada Vietnam", "title": "Senior Backend Developer", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Rejected", "days_ago": 50,
            "salary_min": 32000000, "salary_max": 55000000,
            "url": "https://www.lazada.vn/careers/senior-backend",
            "contact": ("Lê Văn Phúc", "phuc.le@lazada.com", "0934-567-890"),
            "description": "E-commerce platform development. Không match về kinh nghiệm Microservices quy mô lớn."
        },
        {
            "company": "VinFast", "title": "Python Developer (Automotive)", "location": "Hà Nội",
            "source": "TopCV", "work_type": "Onsite", "status": "Rejected", "days_ago": 48,
            "salary_min": 25000000, "salary_max": 42000000,
            "url": "https://vinfastauto.com/careers/python-automotive",
            "contact": ("Phạm Văn Sơn", "son.pham@vinfast.vn", "0945-678-901"),
            "description": "Connected car platform. Thiếu kinh nghiệm về IoT và automotive domain."
        },
        {
            "company": "VPBank", "title": "Tech Lead (Core Banking)", "location": "Hà Nội",
            "source": "VietnamWorks", "work_type": "Onsite", "status": "Rejected", "days_ago": 45,
            "salary_min": 40000000, "salary_max": 70000000,
            "url": "https://www.vpbank.com.vn/careers/tech-lead",
            "contact": ("Nguyễn Thị Linh", "linh.nguyen@vpbank.com.vn", "0956-789-012"),
            "description": "Lead banking transformation. Yêu cầu 7+ năm, không đủ kinh nghiệm leadership."
        },
        {
            "company": "Fossil Vietnam", "title": "Software Engineer (Backend)", "location": "TP.HCM",
            "source": "LinkedIn", "work_type": "Hybrid", "status": "Rejected", "days_ago": 40,
            "salary_min": 20000000, "salary_max": 35000000,
            "url": "https://fossil.com/careers/vietnam/software-engineer",
            "contact": ("Hoàng Văn Minh", "minh.hoang@fossil.com", "0967-890-123"),
            "description": "Retail & e-commerce systems. Offer từ chỗ khác, từ chối tiếp tục process."
        },
        {
            "company": "Sun Asterisk", "title": "Python Developer (Offshore)", "location": "Hà Nội",
            "source": "ITviec", "work_type": "Onsite", "status": "Rejected", "days_ago": 38,
            "salary_min": 18000000, "salary_max": 30000000,
            "url": "https://sun-asterisk.com/careers/python-developer",
            "contact": ("Đỗ Thị Thảo", "thao.do@sun-asterisk.com", "0978-901-234"),
            "description": "Offshore projects cho Nhật. Cultural fit không phù hợp với môi trường Nhật."
        },
    ]
    
    jobs = []
    for idx, data in enumerate(companies_data):
        applied_date = date.today() - timedelta(days=data["days_ago"])
        
        # Calculate deadline
        if data["status"] not in ["Rejected", "Hired"]:
            deadline = applied_date + timedelta(days=random.randint(30, 60))
        else:
            deadline = None
        
        job = Job(
            company_name=data["company"],
            job_title=data["title"],
            location=data["location"],
            work_type=data["work_type"],
            salary_min=data["salary_min"],
            salary_max=data["salary_max"],
            salary_currency="VND",
            source=data["source"],
            current_status=data["status"],
            applied_date=applied_date,
            deadline=deadline,
            is_favorite=data["status"] in ["Offer", "Interview", "Hired"],
            job_url=data["url"],
            job_description=data["description"],
            contact_person=data["contact"][0],
            contact_email=data["contact"][1],
            contact_phone=data["contact"][2]
        )
        db.add(job)
        jobs.append(job)
    
    db.commit()
    print(f"✅ Created {len(jobs)} realistic jobs with comprehensive data")
    print(f"   📊 Status breakdown: Applied({sum(1 for j in jobs if j.current_status=='Applied')}), "
          f"Screening({sum(1 for j in jobs if j.current_status=='Screening')}), "
          f"Interview({sum(1 for j in jobs if j.current_status=='Interview')}), "
          f"Offer({sum(1 for j in jobs if j.current_status=='Offer')}), "
          f"Hired({sum(1 for j in jobs if j.current_status=='Hired')}), "
          f"Rejected({sum(1 for j in jobs if j.current_status=='Rejected')})")
    return jobs


def seed_applications(db, jobs):
    """Seed comprehensive application history with realistic timeline"""
    application_notes = {
        "Applied": [
            "Đã nộp hồ sơ qua {}. CV đã được cập nhật phiên bản mới nhất, kèm cover letter tùy chỉnh cho vị trí này.",
            "Submit application qua {}. Portfolio và GitHub profile đã được đính kèm trong CV.",
            "Nộp hồ sơ thành công qua {}. Đã gửi kèm recommendation letter từ cựu giám đốc.",
        ],
        "Screening": [
            "✅ Nhận được phản hồi từ HR {}. Hồ sơ đang được xem xét bởi hiring manager.",
            "📧 Email từ {}. HR confirm đã nhận hồ sơ, dự kiến sẽ có feedback trong 5-7 ngày.",
            "📞 HR {} gọi điện xác nhận thông tin. Hỏi về experience và expected salary.",
        ],
        "Interview": [
            "🎯 Vượt qua vòng screening! Được mời phỏng vấn technical round với team lead.",
            "✅ Hoàn thành vòng 1 (HR interview). Tiếp tục vòng 2: technical assessment & coding challenge.",
            "🔥 Đã complete technical interview. Team feedback rất tích cực, chờ final round.",
        ],
        "Offer": [
            "🎉 Nhận được offer từ HR! Gross salary: {}, benefits: 13th month, health insurance, laptop.",
            "💰 OFFER RECEIVED! Package: {} + performance bonus 2 months. Đang review và cân nhắc.",
            "✨ Official offer letter đã về! Deadline accept: 5 ngày. Đang so sánh với offers khác.",
        ],
        "Hired": [
            "🚀 ĐÃ CHẤP NHẬN OFFER! Ký hợp đồng hoàn tất. Onboarding date: {}. Chuẩn bị bắt đầu chapter mới!",
            "✅ HIRED! Contract signed. Start date: {}. HR đã gửi onboarding checklist và team introduction.",
            "🎊 Chính thức join team! First day: {}. Rất excited cho dự án mới và team mới!",
        ],
        "Rejected": [
            "❌ Nhận email từ chối. Feedback: 'Excellent skills but looking for more senior profile'. Học hỏi và move on!",
            "😔 Không pass final round. Lý do: Cultural fit. Một vài câu trả lời chưa thể hiện được teamwork spirit.",
            "⚠️ Rejected after technical test. Feedback: Code quality tốt nhưng thiếu optimization và edge case handling.",
            "📧 HR thông báo đã chọn candidate khác. Họ có background match hơn về domain knowledge.",
            "❌ Không tiếp tục process. Lý do cá nhân: Đã nhận offer từ công ty khác với package tốt hơn.",
        ]
    }
    
    count = 0
    for job in jobs:
        # Initial application
        app = Application(
            job_id=job.id,
            status="Applied",
            notes=random.choice(application_notes["Applied"]).format(job.source),
            status_date=job.applied_date
        )
        db.add(app)
        count += 1
        
        # Add progression based on current status
        if job.current_status in ["Screening", "Interview", "Offer", "Hired", "Rejected"]:
            screening_date = job.applied_date + timedelta(days=random.randint(3, 7))
            app2 = Application(
                job_id=job.id,
                status="Screening",
                notes=random.choice(application_notes["Screening"]).format(job.contact_person or "HR"),
                status_date=screening_date
            )
            db.add(app2)
            count += 1
        
        if job.current_status in ["Interview", "Offer", "Hired"]:
            interview_date = job.applied_date + timedelta(days=random.randint(10, 18))
            app3 = Application(
                job_id=job.id,
                status="Interview",
                notes=random.choice(application_notes["Interview"]),
                status_date=interview_date
            )
            db.add(app3)
            count += 1
        
        if job.current_status in ["Offer", "Hired"]:
            offer_date = job.applied_date + timedelta(days=random.randint(25, 35))
            salary_range = f"{job.salary_min:,.0f} - {job.salary_max:,.0f} VND"
            app4 = Application(
                job_id=job.id,
                status="Offer",
                notes=random.choice(application_notes["Offer"]).format(salary_range),
                status_date=offer_date
            )
            db.add(app4)
            count += 1
        
        if job.current_status == "Hired":
            hired_date = job.applied_date + timedelta(days=random.randint(40, 50))
            start_date = (hired_date + timedelta(days=14)).strftime("%d/%m/%Y")
            app5 = Application(
                job_id=job.id,
                status="Hired",
                notes=random.choice(application_notes["Hired"]).format(start_date),
                status_date=hired_date
            )
            db.add(app5)
            count += 1
        
        if job.current_status == "Rejected":
            rejected_date = job.applied_date + timedelta(days=random.randint(8, 30))
            app_rejected = Application(
                job_id=job.id,
                status="Rejected",
                notes=random.choice(application_notes["Rejected"]),
                status_date=rejected_date
            )
            db.add(app_rejected)
            count += 1
    
    db.commit()
    print(f"✅ Created {count} application records with realistic timeline and notes")


def seed_interviews(db, jobs):
    """Seed comprehensive interview data with realistic scenarios"""
    interview_scenarios = {
        "Phone Screening": [
            ("Ms. Nguyễn Thu Hương - HR Manager", "https://meet.google.com/abc-defg-hij", 
             "Passed", "✅ Candidate có communication skills tốt. Background match với JD. Tiếp tục technical round."),
            ("Mr. Trần Minh Khoa - Talent Acquisition", "https://teams.microsoft.com/meet/xyz123",
             "Passed", "✅ Nhiệt tình, motivation cao. Expected salary phù hợp với budget. Move to next round."),
            ("Ms. Lê Thị Mai - Senior Recruiter", "https://zoom.us/j/123456789",
             "Passed", "✅ Ứng viên có exp tốt về Python & FastAPI. Culture fit khá tốt. Recommend technical interview."),
        ],
        "Technical Test": [
            ("Mr. Phạm Văn Long - Tech Lead", "https://meet.google.com/tech-test-001",
             "Passed", "✅ Code quality tốt, clean code principles. Giải quyết được 8/10 problems. Time complexity excellent."),
            ("Ms. Hoàng Thị Mai - Senior Developer", "https://zoom.us/j/technical-987",
             "Passed", "✅ Strong algorithm skills. Handle edge cases tốt. Code dễ đọc, có comments hợp lý."),
            ("Mr. Đỗ Văn Hùng - Engineering Manager", "https://teams.microsoft.com/tech-round",
             "Pending", "🔄 Đang review coding challenge submission. Overall impression: positive, cần thêm thời gian để evaluate."),
        ],
        "System Design": [
            ("Mr. Nguyễn Văn Thành - Solution Architect", "https://meet.google.com/sys-design-01",
             "Passed", "✅ Design scalable system tốt. Hiểu rõ trade-offs. Có exp thực tế với microservices & distributed systems."),
            ("Ms. Vũ Thị Lan - Principal Engineer", "https://zoom.us/j/system-design-456",
             "Passed", "✅ Approach hợp lý cho high-traffic system. Biết cách handle bottlenecks. Security awareness tốt."),
        ],
        "Final Round": [
            ("Mr. Lê Văn Đức - Engineering Director", "https://meet.google.com/final-xyz",
             "Passed", "🎯 Excellent candidate! Technical strong, culture fit tốt, leadership potential. Recommend to hire."),
            ("Ms. Trần Thị Nga - CTO", "https://teams.microsoft.com/final-round",
             "Passed", "🌟 Outstanding performance across all rounds. Vision alignment với company goals. Definitely make offer!"),
            ("Mr. Hoàng Văn Tùng - VP Engineering", "https://zoom.us/j/final-interview",
             "Passed", "✅ Great addition to the team. Technical depth và breadth đều tốt. Team will benefit from his experience."),
        ]
    }
    
    count = 0
    for job in jobs:
        # Jobs in Interview/Offer/Hired status: Add completed interview rounds
        if job.current_status in ["Interview", "Offer", "Hired"]:
            # Round 1: Phone Screening
            phone_interviewer, phone_link, phone_result, phone_feedback = random.choice(interview_scenarios["Phone Screening"])
            interview1 = Interview(
                job_id=job.id,
                round_number=1,
                interview_type="Phone Screening",
                scheduled_date=job.applied_date + timedelta(days=random.randint(5, 9)),
                meeting_link=phone_link,
                interviewer_name=phone_interviewer,
                result=phone_result,
                feedback=phone_feedback
            )
            db.add(interview1)
            count += 1
            
            # Round 2: Technical Test/Interview
            tech_interviewer, tech_link, tech_result, tech_feedback = random.choice(interview_scenarios["Technical Test"])
            interview2 = Interview(
                job_id=job.id,
                round_number=2,
                interview_type=random.choice(["Technical Test", "Coding Challenge", "Technical Interview"]),
                scheduled_date=job.applied_date + timedelta(days=random.randint(12, 18)),
                meeting_link=tech_link,
                interviewer_name=tech_interviewer,
                result="Passed" if job.current_status in ["Offer", "Hired"] else tech_result,
                feedback=tech_feedback
            )
            db.add(interview2)
            count += 1
            
            # Round 3: System Design (for Interview/Offer/Hired with more rounds)
            if job.current_status in ["Offer", "Hired"] or random.random() > 0.5:
                sys_interviewer, sys_link, sys_result, sys_feedback = random.choice(interview_scenarios["System Design"])
                interview3 = Interview(
                    job_id=job.id,
                    round_number=3,
                    interview_type="System Design",
                    scheduled_date=job.applied_date + timedelta(days=random.randint(19, 25)),
                    meeting_link=sys_link,
                    interviewer_name=sys_interviewer,
                    result="Passed" if job.current_status in ["Offer", "Hired"] else "Pending",
                    feedback=sys_feedback
                )
                db.add(interview3)
                count += 1
            
            # Round 4: Final Round (only for Offer/Hired)
            if job.current_status in ["Offer", "Hired"]:
                final_interviewer, final_link, final_result, final_feedback = random.choice(interview_scenarios["Final Round"])
                interview4 = Interview(
                    job_id=job.id,
                    round_number=4,
                    interview_type="Final Round",
                    scheduled_date=job.applied_date + timedelta(days=random.randint(26, 33)),
                    meeting_link=final_link,
                    interviewer_name=final_interviewer,
                    result=final_result,
                    feedback=final_feedback
                )
                db.add(interview4)
                count += 1
        
        # Jobs in Screening status: Add upcoming interview
        elif job.current_status == "Screening":
            scheduled = date.today() + timedelta(days=random.randint(3, 10))
            upcoming_interviewer, upcoming_link, _, _ = random.choice(interview_scenarios["Phone Screening"])
            interview = Interview(
                job_id=job.id,
                round_number=1,
                interview_type="Phone Screening",
                scheduled_date=scheduled,
                meeting_link=upcoming_link,
                interviewer_name=upcoming_interviewer,
                result="Pending",
                feedback=None
            )
            db.add(interview)
            count += 1
    
    db.commit()
    print(f"✅ Created {count} interview records with realistic scenarios and feedback")


def seed_notes(db, jobs):
    """Seed notes for various jobs with realistic content"""
    note_templates = {
        "Research": [
            ("Company Culture Research", "Glassdoor rating: 4.3/5 ⭐. Pros: Good work-life balance, modern tech stack, learning culture. Cons: Salary slightly below market for seniors. Employee reviews mention great team collaboration."),
            ("Tech Stack Analysis", "Tech Stack: Python 3.11, FastAPI, PostgreSQL, Redis, Docker, K8s, AWS/GCP. Microservices architecture. CI/CD with GitLab. Monitoring: Prometheus + Grafana. Match: 90% với skillset hiện tại."),
            ("Company Financial Info", "Company vừa raise được Series B $20M. Revenue growth 150% YoY. Headcount: ~200 employees. Stable và có tiềm năng scale. Product-market fit tốt trong Fintech domain."),
            ("Team & Project Info", "Team: 8-10 engineers (3 seniors, 5 mids, 2 juniors). Project: Building next-gen payment platform. Tech challenges: High throughput (10K TPS), low latency (<100ms), data consistency."),
        ],
        "Preparation": [
            ("Interview Prep Checklist", "✅ Review Python advanced topics (decorators, metaclasses, async/await)\n✅ Ôn System Design patterns (CQRS, Event Sourcing, Circuit Breaker)\n✅ Practice coding challenges (LeetCode medium/hard)\n⏳ Mock interview with mentor\n⏳ Chuẩn bị STAR stories cho behavioral questions"),
            ("Technical Topics to Study", "1. FastAPI internals & best practices\n2. Database optimization (indexing, query planning, N+1 problem)\n3. Microservices patterns & distributed systems\n4. Caching strategies (Redis patterns)\n5. Message queues (Kafka/RabbitMQ)\n6. Container orchestration (K8s basics)"),
            ("Behavioral Questions Prep", "Questions có thể hỏi:\n- Tell me about a challenging bug you fixed\n- How do you handle tight deadlines?\n- Describe a time you disagreed with a team member\n- Your biggest technical achievement?\n\nChuẩn bị STAR format: Situation, Task, Action, Result"),
        ],
        "Salary Negotiation": [
            ("Compensation Strategy", "💰 Current: 28M gross\n🎯 Target: 35-40M gross (+25-40%)\n📊 Market rate for 5 YoE Senior: 32-45M\n💡 Negotiation points: Python exp, Microservices exp, Past performance\n⚠️ Acceptable minimum: 32M + good benefits"),
            ("Benefits to Negotiate", "Priority benefits:\n✅ Flexible remote/hybrid (3 days WFH)\n✅ Health insurance for family\n✅ Learning budget (10-15M/year)\n✅ Performance bonus (2-3 months)\n✅ Stock options/ESOP\n✅ Modern equipment (MacBook Pro M3)"),
            ("Market Research", "Market data:\n- Mid-level (3-5 YoE): 20-32M\n- Senior (5-7 YoE): 32-50M\n- Lead (7+ YoE): 50-80M\n\nCompany size factor:\n- Startup: Higher risk, stock options\n- Mid-size: Balanced\n- Corp: Stable, good benefits"),
        ],
        "Follow Up": [
            ("Post-Interview Follow-up", "✅ Đã gửi thank you email trong 24h sau interview\n📧 Email gửi tới: {} & hiring manager\n📅 HR hẹn feedback: 3-5 ngày làm việc\n🔔 Reminder: Follow up nếu sau 7 ngày chưa có tin"),
            ("Application Status Check", "📍 Timeline:\n- Applied: {}\n- Last update: {} (Screening)\n- Next step: Technical interview (dự kiến trong 1-2 tuần)\n\n🔔 Action: Gửi follow-up email nếu sau 10 ngày chưa nghe tin"),
            ("Interview Debrief", "Self-assessment sau interview:\n✅ Strengths: Technical questions trả lời tốt, enthusiasm high\n⚠️ Areas to improve: System design câu trả lời có thể detail hơn\n💭 Impression: Team friendly, vibe tốt, có thể fit văn hóa\n🎯 Confidence level: 75% pass round này"),
        ],
        "General": [
            ("Position Analysis", "📋 Role: {}\n🎯 Match score: 85%\n✅ Pros: Modern tech, good team, growth opportunity\n⚠️ Cons: Onsite 5 days/week, commute time 45 mins\n💡 Decision factors: Salary package, team culture, career path"),
            ("Pros & Cons", "✅ PROS:\n- Tech stack alignment\n- Company growth trajectory\n- Learning opportunities\n- Team experience level\n\n❌ CONS:\n- Salary slightly below expectation\n- Location (commute time)\n- Not much remote flexibility"),
            ("Career Goals Alignment", "🎯 Short-term goals (1-2 years):\n- Master microservices at scale\n- Lead small team (2-3 members)\n- Deep dive vào distributed systems\n\n🚀 Long-term (3-5 years):\n- Tech Lead / Engineering Manager\n- Architecture expertise\n- Speaking/Writing tech content\n\n✅ Alignment: Position này support được 80% goals"),
        ],
        "Interview Prep": [
            ("Common Python Questions", "1. Difference between list/tuple/set/dict?\n2. Explain decorators with example\n3. What is GIL? Impact on multithreading?\n4. Async/await vs threading?\n5. Memory management & garbage collection\n6. Mutable vs immutable objects\n7. *args vs **kwargs\n8. Context managers (with statement)"),
            ("System Design Questions", "Potential questions:\n1. Design URL shortener (like bit.ly)\n2. Design rate limiter\n3. Design notification system\n4. Design payment processing system\n5. Design real-time chat\n\nKey concepts: Scalability, CAP theorem, Load balancing, Caching, Database sharding"),
            ("Coding Challenge Topics", "Focus areas:\n- Array/String manipulation\n- Hash Tables\n- Two pointers technique\n- Sliding window\n- Binary search\n- Tree/Graph traversal\n- Dynamic programming (basic)\n- Time/Space complexity analysis"),
        ]
    }
    
    priorities = ["Low", "Medium", "High"]
    
    count = 0
    # Add notes for jobs in active stages (not Rejected)
    active_jobs = [j for j in jobs if j.current_status != "Rejected"]
    
    for job in active_jobs[:15]:  # Add notes for first 15 active jobs
        # Determine number of notes based on job status
        if job.current_status in ["Offer", "Hired"]:
            num_notes = random.randint(4, 6)  # More notes for important jobs
        elif job.current_status == "Interview":
            num_notes = random.randint(3, 5)
        else:
            num_notes = random.randint(2, 4)
        
        # Select note types
        note_types = random.sample(list(note_templates.keys()), min(num_notes, len(note_templates)))
        
        for note_type in note_types:
            title, content = random.choice(note_templates[note_type])
            
            # Customize content with job-specific info
            if "{}" in content:
                if "follow-up" in title.lower():
                    content = content.format(job.contact_email or "HR team")
                elif "Applied:" in content:
                    content = content.format(
                        job.applied_date.strftime("%d/%m/%Y"),
                        (job.applied_date + timedelta(days=random.randint(3, 7))).strftime("%d/%m/%Y")
                    )
                elif "Role:" in content:
                    content = content.format(job.job_title)
            
            # Set priority based on job status and note type
            if job.current_status in ["Offer", "Interview"]:
                priority = "High" if note_type in ["Preparation", "Salary Negotiation", "Follow Up"] else "Medium"
            elif job.current_status == "Screening":
                priority = "Medium" if note_type in ["Preparation", "Research"] else "Low"
            else:
                priority = random.choice(["Low", "Medium"])
            
            note = Note(
                job_id=job.id,
                note_type=note_type,
                title=title,
                content=content,
                priority=priority
            )
            db.add(note)
            count += 1
    
    db.commit()
    print(f"✅ Created {count} realistic notes with detailed content")


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
    """Seed database with realistic and comprehensive data"""
    print("🌱 Seeding database with realistic sample data...")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        jobs = seed_jobs(db)
        seed_applications(db, jobs)
        seed_interviews(db, jobs)
        seed_notes(db, jobs)
        seed_email_templates(db)
        
        print("=" * 70)
        print("\n🎉 Database seeded successfully with comprehensive realistic data!")
        
        # Calculate statistics
        status_counts = {}
        for job in jobs:
            status_counts[job.current_status] = status_counts.get(job.current_status, 0) + 1
        
        print(f"""
📊 SUMMARY:
   
   Jobs Created: {len(jobs)} jobs
   ├─ Applied: {status_counts.get('Applied', 0)} jobs (Recently submitted)
   ├─ Screening: {status_counts.get('Screening', 0)} jobs (Under review)
   ├─ Interview: {status_counts.get('Interview', 0)} jobs (Interview rounds)
   ├─ Offer: {status_counts.get('Offer', 0)} jobs (Offer received)
   ├─ Hired: {status_counts.get('Hired', 0)} jobs (Accepted offer)
   └─ Rejected: {status_counts.get('Rejected', 0)} jobs (Not selected)
   
   📋 Application history: Full timeline with realistic notes
   🎯 Interview records: Multiple rounds with detailed feedback
   📝 Notes: Research, prep, negotiation tips
   ✉️ Email templates: Ready-to-use templates
   
   🏢 Companies: Real Vietnamese tech companies
   💰 Salaries: Realistic ranges (18M - 70M VND)
   📍 Locations: Hà Nội, TP.HCM, Đà Nẵng
   👥 Contacts: Sample HR contacts for each position
        """)
        
    except Exception as e:
        print(f"\n❌ Error occurred during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
