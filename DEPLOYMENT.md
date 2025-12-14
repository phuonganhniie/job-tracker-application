# 🚀 Deployment Guide - Job Tracker Application

## 📋 Tổng Quan

Hướng dẫn deploy monorepo application lên Render.com (free tier) với:
- **Backend**: FastAPI + PostgreSQL
- **Frontend**: Streamlit
- **Auto-seed**: Tự động tạo dữ liệu demo khi database rỗng

---

## 🏗️ Kiến Trúc Deployment

```
┌─────────────────────────────────────────────────┐
│          Render.com (Free Tier)                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │   Backend    │◄────────┤   PostgreSQL    │  │
│  │   FastAPI    │         │   Database      │  │
│  │  Port 8000   │         │                 │  │
│  └──────┬───────┘         └─────────────────┘  │
│         │                                       │
│         │ API Calls                             │
│         ▼                                       │
│  ┌──────────────┐                              │
│  │   Frontend   │                              │
│  │  Streamlit   │                              │
│  │  Port 8501   │                              │
│  └──────────────┘                              │
│                                                 │
└─────────────────────────────────────────────────┘
         ▲
         │ HTTP Monitoring (5 min interval)
         │
    ┌────┴────┐
    │ Uptime  │
    │ Robot   │
    └─────────┘
```

---

## 📦 Prerequisites

### 1. Chuẩn Bị Code
```bash
# File cấu trúc quan trọng
job-tracker-application/
├── render.yaml                 # Render Blueprint
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── backend/
│   ├── main.py                # FastAPI entry point
│   ├── core/config.py         # Settings & environment variables
│   └── ...
├── frontend/
│   ├── Home.py                # Streamlit entry point
│   └── ...
└── scripts/
    └── seed_db_prod.py        # Production seed data
```

### 2. Chuẩn Bị GitHub
- Repository phải là **public** (hoặc connect private repo với GitHub OAuth)
- Push code lên branch `feature/deploy-to-cloud` hoặc `main`

### 3. Chuẩn Bị Render Account
- Đăng ký tại: https://render.com (free tier)
- Connect GitHub account

---

## 🎯 Deployment Flow

### **Phase 1: Setup Render Blueprint**

#### Bước 1: Tạo `render.yaml`
File này định nghĩa toàn bộ infrastructure:

```yaml
services:
  # Backend Service
  - type: web
    name: job-tracker-backend
    runtime: python
    region: singapore
    plan: free
    branch: feature/deploy-to-cloud
    rootDir: .
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: job-tracker-db
          property: connectionString
      - key: BACKEND_CORS_ORIGINS
        value: '["https://job-tracker-frontend.onrender.com"]'
      - key: AUTO_SEED_DB
        value: "true"
    healthCheckPath: /docs

  # Frontend Service
  - type: web
    name: job-tracker-frontend
    runtime: python
    region: singapore
    plan: free
    branch: feature/deploy-to-cloud
    rootDir: .
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run frontend/Home.py --server.port 8501 --server.address 0.0.0.0
    envVars:
      - key: API_BASE_URL
        value: https://job-tracker-backend.onrender.com

databases:
  - name: job-tracker-db
    databaseName: job_tracker
    region: singapore
    plan: free
    user: job_tracker_user
```

#### Bước 2: Deploy từ Render Dashboard
1. Vào **Render Dashboard** → **Blueprints**
2. Click **"New Blueprint Instance"**
3. Connect GitHub repository
4. Select branch: `feature/deploy-to-cloud`
5. Render sẽ tự động detect `render.yaml` và tạo:
   - ✅ PostgreSQL database
   - ✅ Backend service
   - ✅ Frontend service

---

### **Phase 2: Environment Variables**

Render tự động set các env vars từ `render.yaml`, nhưng có thể override:

#### Backend Environment Variables
| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | Auto from DB | PostgreSQL connection string |
| `BACKEND_CORS_ORIGINS` | `["https://job-tracker-frontend.onrender.com"]` | Frontend URL cho CORS |
| `AUTO_SEED_DB` | `true` | Enable auto-seed khi DB rỗng |

#### Frontend Environment Variables
| Variable | Value | Description |
|----------|-------|-------------|
| `API_BASE_URL` | `https://job-tracker-backend.onrender.com` | Backend API endpoint |

---

### **Phase 3: Auto-Seed Mechanism**

#### Flow Diagram
```
Backend Startup
    │
    ▼
Check if DB empty?
    │
    ├─ NO ──► Skip seed ──► App ready
    │
    └─ YES ──► AUTO_SEED_DB = true?
                    │
                    ├─ NO ──► Skip seed ──► App ready
                    │
                    └─ YES ──► Run seed functions
                                    │
                                    ├─► seed_jobs(7)
                                    ├─► seed_interviews(2)
                                    ├─► seed_notes(4)
                                    ├─► seed_applications(3)
                                    └─► seed_email_templates(3)
                                            │
                                            ▼
                                    Auto-seed complete ✅
                                            │
                                            ▼
                                    App ready 🚀
```

#### Code Implementation (`backend/main.py`)
```python
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    
    # Auto-seed database if empty
    try:
        from backend.core.database import SessionLocal
        from backend.models.job import Job
        import os
        
        db = SessionLocal()
        job_count = db.query(Job).count()
        
        auto_seed = os.getenv("AUTO_SEED_DB", "true").lower() == "true"
        
        if job_count == 0 and auto_seed:
            logger.info("🌱 Database is empty, running auto-seed...")
            
            from scripts.seed_db_prod import (
                seed_jobs, seed_interviews, seed_notes,
                seed_applications, seed_email_templates
            )
            
            jobs = seed_jobs(db)
            interviews = seed_interviews(db, jobs)
            seed_notes(db, jobs, interviews)
            seed_applications(db, jobs)
            seed_email_templates(db)
            
            logger.info("✅ Auto-seed completed successfully")
    except Exception as e:
        logger.error(f"⚠️ Auto-seed failed: {e}")
```

---

### **Phase 4: Database Seeding**

#### Seed Data Structure

**1. Jobs (7 records)**
- VNG Corporation - Backend Developer (Applied)
- Tiki - Python Developer (Phone Screening)
- FPT Software - Junior Backend Developer (Applied)
- Shopee Vietnam - Backend Engineer Intern (Offer)
- Momo - Software Engineer Backend (Offer)
- Base.vn - Backend Engineer (Rejected)
- KiotViet - Backend Developer (Archived)

**2. Interviews (2 records)**
- VNG Phone Screening (Passed - 7 days ago)
- VNG Technical Interview (Pending - 3 days from now)

**3. Notes (4 records)**
- Shopee offer deadline reminder
- Momo best offer consideration
- Base.vn feedback note
- VNG interview preparation

**4. Applications (3 records)**
- VNG status history: Applied → Screening → Interview

**5. Email Templates (3 records)**
- Thank You After Interview
- Application Status Follow-up
- Offer Acceptance

#### Re-seed Strategy (nếu cần)

**Cách 1: Xóa data từ Render Dashboard**
```sql
-- Connect to database via external connection
TRUNCATE TABLE notes, applications, interviews, email_templates, jobs CASCADE;
```

**Cách 2: Xóa và tái tạo database**
1. Render Dashboard → Database → Settings → Delete Database
2. Tạo lại database mới
3. Update DATABASE_URL trong backend service
4. Redeploy backend → auto-seed sẽ chạy

---

## 🔄 CI/CD Workflow

### Auto-Deploy Process
```
Git Push
    │
    ▼
GitHub (feature/deploy-to-cloud)
    │
    ▼
Render Webhook Triggered
    │
    ├─► Backend Build
    │   ├─ Install dependencies
    │   ├─ Run health check
    │   └─ Deploy
    │
    └─► Frontend Build
        ├─ Install dependencies
        ├─ Start Streamlit
        └─ Deploy
```

### Manual Deploy
1. Render Dashboard → Service → **"Manual Deploy"**
2. Select **"Clear build cache & deploy"** (nếu cần)
3. Monitor logs trong **"Logs"** tab

---

## 🔍 Monitoring & Health Check

### Health Check Endpoints
- **Backend**: `https://job-tracker-backend.onrender.com/docs`
- **Frontend**: `https://job-tracker-frontend.onrender.com/`

### Logs Monitoring
```bash
# View real-time logs
Render Dashboard → Service → Logs tab

# Key log patterns
✅ "Auto-seed completed successfully"
✅ "Application startup complete"
❌ "Auto-seed failed"
❌ "Database connection error"
```

---

## 🤖 UptimeRobot Setup (Keep Awake)

### Vấn Đề: Free Tier Sleep
- Render free tier sleep sau **15 phút idle**
- Cold start mất **30-50 giây** để wake up

### Giải Pháp: Ping Định Kỳ

#### Bước 1: Tạo UptimeRobot Account
- Đăng ký tại: https://uptimerobot.com (free)
- Free tier: **50 monitors**, ping interval **5 phút**

#### Bước 2: Tạo Monitor cho Backend
1. Dashboard → **"+ Add New Monitor"**
2. **Monitor Type**: HTTP(s)
3. **Friendly Name**: `Job Tracker Backend`
4. **URL**: `https://job-tracker-backend.onrender.com/docs`
5. **Monitoring Interval**: **5 minutes**
6. **Monitor Timeout**: 30 seconds
7. **Alert Contacts**: Your email
8. Click **"Create Monitor"**

#### Bước 3: Tạo Monitor cho Frontend
1. **Monitor Type**: HTTP(s)
2. **Friendly Name**: `Job Tracker Frontend`
3. **URL**: `https://job-tracker-frontend.onrender.com/`
4. **Monitoring Interval**: **5 minutes**
5. Click **"Create Monitor"**

#### Bước 4: Verify
- Kiểm tra **"Status"** column → Phải là **"Up"**
- Response time thường: **100-500ms** (sau khi warm)
- First request: **30-50 seconds** (cold start)

### UptimeRobot Configuration Summary
```yaml
Backend Monitor:
  URL: https://job-tracker-backend.onrender.com/docs
  Interval: 5 minutes
  Timeout: 30 seconds
  Expected Status: 200 OK
  
Frontend Monitor:
  URL: https://job-tracker-frontend.onrender.com/
  Interval: 5 minutes
  Timeout: 30 seconds
  Expected Status: 200 OK
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **CORS Error**
```
Access to fetch at 'https://backend.onrender.com' from origin 'https://frontend.onrender.com' has been blocked by CORS policy
```

**Fix**: Cập nhật `BACKEND_CORS_ORIGINS` trong render.yaml
```yaml
- key: BACKEND_CORS_ORIGINS
  value: '["https://job-tracker-frontend.onrender.com"]'
```

#### 2. **Database Connection Error**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Fix**: Kiểm tra DATABASE_URL
```bash
# Render Dashboard → Database → Info → Internal Connection String
# Update backend service env var
```

#### 3. **Auto-seed Không Chạy**
```
Database already has X jobs, skipping auto-seed
```

**Fix**: Xóa data và redeploy
```sql
TRUNCATE TABLE jobs CASCADE;
```

#### 4. **Field Name Errors**
```
TypeError: 'name' is an invalid keyword argument for EmailTemplate
```

**Fix**: Kiểm tra model field names
```python
# ❌ Wrong
EmailTemplate(name="Template", category="type")

# ✅ Correct  
EmailTemplate(template_name="Template", template_type="type")
```

#### 5. **Service Sleep Issue**
```
App không response sau 15 phút
```

**Fix**: Setup UptimeRobot (xem section trên)

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] `render.yaml` configured
- [ ] Environment variables set
- [ ] Database models migrated
- [ ] Seed data ready
- [ ] CORS origins updated

### Deployment
- [ ] GitHub repo connected
- [ ] Blueprint instance created
- [ ] Database provisioned
- [ ] Backend deployed
- [ ] Frontend deployed

### Post-Deployment
- [ ] Health checks passing
- [ ] Auto-seed completed
- [ ] Frontend can call backend
- [ ] Data displays correctly
- [ ] UptimeRobot monitors active

### Monitoring
- [ ] Logs clean (no errors)
- [ ] Response time < 500ms
- [ ] Uptime > 99%
- [ ] Email alerts configured

---

## 🔗 Links & Resources

### Deployed URLs
- **Backend API**: https://job-tracker-backend.onrender.com
- **API Docs**: https://job-tracker-backend.onrender.com/docs
- **Frontend**: https://job-tracker-frontend.onrender.com

### Documentation
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Streamlit Docs: https://docs.streamlit.io
- UptimeRobot Docs: https://uptimerobot.com/help

### Tools
- Render Dashboard: https://dashboard.render.com
- UptimeRobot Dashboard: https://uptimerobot.com/dashboard
- GitHub Actions: https://github.com/features/actions

---

## 📝 Notes

### Free Tier Limitations
- ⏱️ **Sleep after 15 min**: Use UptimeRobot để giữ awake
- 🐌 **Cold start**: 30-50 seconds wake-up time
- 💾 **Database**: 1GB storage limit
- 🔄 **Build time**: ~2-3 phút mỗi deploy
- 📊 **Monthly hours**: 750 hours/month (đủ cho 1 service 24/7)

### Best Practices
1. **Minimize cold starts**: Setup monitoring ping 5 phút/lần
2. **Optimize dependencies**: Chỉ install packages cần thiết
3. **Monitor logs**: Check logs sau mỗi deploy
4. **Test locally first**: Đảm bảo code chạy ok trước khi push
5. **Use environment variables**: Không hardcode credentials

### Future Improvements
- [ ] Thêm Redis caching
- [ ] Setup GitHub Actions CI/CD
- [ ] Thêm automated tests
- [ ] Migrate to paid tier nếu cần performance
- [ ] Setup custom domain

---

## 👨‍💻 Maintainer

**Project**: Job Tracker Application  
**Tech Stack**: FastAPI + Streamlit + PostgreSQL  
**Platform**: Render.com (Free Tier)  
**Repository**: https://github.com/phuonganhniie/job-tracker-application  
**Branch**: `feature/deploy-to-cloud`

---

## 📄 License

Graduation Project - For Educational Purpose
