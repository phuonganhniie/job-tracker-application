# 🚀 DEPLOYMENT GUIDE - Job Tracker Application

Hướng dẫn deploy monorepo lên cloud cho đồ án tốt nghiệp.

---

## 📊 TECH STACK SUMMARY

| Component | Technology | Port | Notes |
|-----------|-----------|------|-------|
| **Backend** | FastAPI + Uvicorn | 8000 | REST API, CORS enabled |
| **Frontend** | Streamlit | 8501 | Python web app, gọi backend qua REST |
| **Database** | PostgreSQL (prod) | 5432 | SQLite for local dev |
| **ORM** | SQLAlchemy 2.0 | - | Auto create tables |

**Key Points:**
- Frontend gọi backend qua `API_BASE_URL` (env var)
- CORS đã config sẵn, support JSON string từ env
- No authentication → đơn giản cho deployment
- Database tự động init tables khi start

---

## 🎯 2 PHƯƠNG ÁN DEPLOY

### **OPTION A: Split Deploy (Heroku + Streamlit Cloud)**

**Platform:**
- Backend: Heroku (với Student Pack)
- Frontend: Streamlit Cloud
- Database: Heroku Postgres

**Ưu điểm:**
- Heroku Student Pack: Free dyno + Postgres add-on
- Streamlit Cloud: Unlimited apps miễn phí
- Setup đơn giản, ít config

**Nhược điểm:**
- Heroku free dyno sleep sau 30 phút → cold start 5-10s
- 2 platform riêng biệt → quản lý phức tạp hơn

**Khi nào dùng:**
- Bạn có Heroku Student Pack
- Ưu tiên stability (Streamlit Cloud uptime tốt)
- Không muốn lo downtime

---

### **OPTION B: Monorepo Deploy (Render - ĐỀ XUẤT)** ⭐

**Platform:** Render.com

**Ưu điểm:**
- ✅ **Miễn phí 100%** (Free tier)
- ✅ Deploy từ 1 repo duy nhất
- ✅ Auto deploy từ GitHub
- ✅ PostgreSQL database built-in
- ✅ SSL/HTTPS tự động
- ✅ Support monorepo tốt nhất

**Nhược điểm:**
- Free tier sleep sau 15 phút idle → cold start 30-50s
- Giới hạn 750 giờ/tháng (đủ cho demo)

**Khi nào dùng:**
- Đồ án tốt nghiệp, demo project
- Không có budget
- Muốn deploy nhanh, ít phức tạp

---

## ✅ HƯỚNG DẪN DEPLOY VỚI RENDER (OPTION B)

### **BƯỚC 1: Chuẩn bị Repository**

#### 1.1. Commit các file cấu hình

```bash
# Check các file đã tạo
git status

# Add các file mới
git add render.yaml
git add requirements-prod.txt
git add scripts/init_db_prod.py
git add backend/core/config.py
git add frontend/config/settings.py

# Commit
git commit -m "feat: Add Render deployment configuration"

# Push lên GitHub
git push origin feature/phase2-interview-functional
```

#### 1.2. Merge vào main/master (hoặc deploy từ branch)

```bash
# Option A: Merge vào main
git checkout main
git merge feature/phase2-interview-functional
git push origin main

# Option B: Deploy trực tiếp từ feature branch (khuyến nghị cho test)
# Không cần merge, Render sẽ deploy từ branch này
```

---

### **BƯỚC 2: Setup Render Account**

1. **Đăng ký Render:**
   - Truy cập: https://render.com
   - Click "Get Started for Free"
   - Sign up bằng GitHub account (khuyến nghị)

2. **Kết nối GitHub:**
   - Render sẽ yêu cầu quyền truy cập repos
   - Chọn "Only select repositories"
   - Chọn repo `job-tracker-application`

---

### **BƯỚC 3: Deploy Backend API**

#### 3.1. Tạo Web Service cho Backend

1. Vào Dashboard → Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Chọn repo: `job-tracker-application`
   - Branch: `feature/phase2-interview-functional` (hoặc `main`)

3. **Configure Service:**
   ```
   Name: job-tracker-backend
   Region: Singapore (gần VN nhất)
   Branch: feature/phase2-interview-functional
   Root Directory: (để trống - monorepo root)
   Runtime: Python 3
   Build Command: pip install -r requirements-prod.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Plan:**
   - Chọn **"Free"** ($0/month)

5. **Environment Variables:**
   Click "Advanced" → Add env vars:
   ```
   PYTHON_VERSION = 3.11.0
   DEBUG = false
   API_V1_PREFIX = /api/v1
   ```

   **⚠️ Chưa thêm DATABASE_URL** (làm bước 3.3 trước)

6. Click **"Create Web Service"** → Đợi build (2-3 phút)

#### 3.2. Tạo PostgreSQL Database

1. Vào Dashboard → Click **"New +"** → **"PostgreSQL"**

2. **Configure Database:**
   ```
   Name: job-tracker-db
   Database Name: job_tracker
   Region: Singapore
   Plan: Free ($0/month)
   ```

3. Click **"Create Database"** → Đợi provision (1-2 phút)

4. **Lấy Connection String:**
   - Click vào database `job-tracker-db`
   - Tab "Info" → Copy **"Internal Database URL"**
   - Format: `postgresql://user:password@host/database`

#### 3.3. Thêm DATABASE_URL vào Backend

1. Quay lại service `job-tracker-backend`
2. Tab "Environment" → Add:
   ```
   DATABASE_URL = postgresql://user:password@host/database
   ```
   (paste connection string vừa copy)

3. **Auto Redeploy** → Backend sẽ restart với DB mới

#### 3.4. Init Database Tables

Backend sẽ tự động tạo tables khi start (nhờ `init_db()` trong `main.py`).

**Verify:**
- Tab "Logs" → xem log:
  ```
  INFO: Application startup complete.
  ```

**Test API:**
- Tab "Overview" → Copy URL (ví dụ: `https://job-tracker-backend.onrender.com`)
- Mở trình duyệt: `https://job-tracker-backend.onrender.com/docs`
- Nếu thấy Swagger UI → ✅ Backend OK

---

### **BƯỚC 4: Deploy Frontend**

#### 4.1. Tạo Web Service cho Frontend

1. Dashboard → Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Cùng repo: `job-tracker-application`
   - Branch: `feature/phase2-interview-functional`

3. **Configure Service:**
   ```
   Name: job-tracker-frontend
   Region: Singapore
   Branch: feature/phase2-interview-functional
   Root Directory: (để trống)
   Runtime: Python 3
   Build Command: pip install -r requirements-prod.txt
   Start Command: streamlit run frontend/Home.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```

4. **Plan:**
   - Chọn **"Free"**

5. **Environment Variables:**
   ```
   PYTHON_VERSION = 3.11.0
   API_BASE_URL = https://job-tracker-backend.onrender.com
   API_V1_PREFIX = /api/v1
   ```
   **⚠️ Thay `job-tracker-backend.onrender.com` bằng URL thật của backend bạn**

6. Click **"Create Web Service"**

#### 4.2. Update CORS cho Backend

Frontend URL mới (ví dụ): `https://job-tracker-frontend.onrender.com`

1. Vào service `job-tracker-backend`
2. Tab "Environment" → Add/Edit:
   ```
   BACKEND_CORS_ORIGINS = ["https://job-tracker-frontend.onrender.com"]
   ```

3. Save → Backend auto redeploy

---

### **BƯỚC 5: Verify Deployment**

#### 5.1. Test Backend

1. Mở: `https://job-tracker-backend.onrender.com/docs`
2. Thử API endpoint: `GET /api/v1/jobs`
3. Nếu trả về `{"items": [], "total": 0}` → ✅ OK

#### 5.2. Test Frontend

1. Mở: `https://job-tracker-frontend.onrender.com`
2. Thử tạo Job mới
3. Check dữ liệu xuất hiện → ✅ OK

#### 5.3. Test Integration

1. Frontend: Tạo job mới
2. Backend API: `GET /api/v1/jobs` → verify job đã lưu
3. Frontend: Reload page → job vẫn còn

---

### **BƯỚC 6: Setup Auto Deploy (CI/CD)**

Render tự động deploy khi push code lên branch đã chọn.

**Cấu hình:**
1. Vào mỗi service → Tab "Settings"
2. Section "Build & Deploy"
3. Enable **"Auto-Deploy"** → Yes
4. Chọn branch: `feature/phase2-interview-functional` hoặc `main`

**Test:**
```bash
# Sửa code
echo "# Test deploy" >> README.md

# Commit + push
git add README.md
git commit -m "test: Trigger auto deploy"
git push origin feature/phase2-interview-functional

# Render sẽ tự động build và deploy
# Check tab "Events" trong Dashboard
```

---

## 🔧 TROUBLESHOOTING

### ❌ Backend không start

**Lỗi:** `ModuleNotFoundError: No module named 'backend'`

**Fix:**
- Check `Root Directory` = (trống)
- Check `Start Command`:
  ```
  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```

---

### ❌ Frontend không kết nối Backend

**Lỗi:** CORS error hoặc "Connection refused"

**Fix:**
1. Check `API_BASE_URL` trong frontend env:
   ```
   API_BASE_URL = https://job-tracker-backend.onrender.com
   ```
   (không có `/` cuối, dùng https)

2. Check `BACKEND_CORS_ORIGINS` trong backend env:
   ```
   BACKEND_CORS_ORIGINS = ["https://job-tracker-frontend.onrender.com"]
   ```

---

### ❌ Database connection failed

**Lỗi:** `could not connect to server`

**Fix:**
- Check `DATABASE_URL` format:
  ```
  postgresql://user:password@host/database
  ```
- Dùng **"Internal Database URL"** (không phải External)
- Verify database status = "Available"

---

### ❌ Cold start chậm

**Hiện tượng:** App mất 30-50s để start sau khi sleep

**Giải pháp:**
1. **Ping service định kỳ** (giữ app awake):
   - Dùng UptimeRobot (free): https://uptimerobot.com
   - Add monitor cho frontend + backend URL
   - Interval: 5 phút

2. **Upgrade plan:**
   - Render: $7/month → no sleep
   - Railway: $5 credit/month → đủ cho 2 services

---

## 📋 CHECKLIST DEPLOY END-TO-END

### Pre-deployment
- [ ] Code đã commit, push lên GitHub
- [ ] File `render.yaml` đã có trong repo
- [ ] File `requirements-prod.txt` có `psycopg2-binary`
- [ ] Backend config hỗ trợ JSON string cho CORS
- [ ] Frontend config đọc `API_BASE_URL` từ env

### Render Setup
- [ ] Đăng ký Render account
- [ ] Kết nối GitHub repository

### Backend Deployment
- [ ] Tạo Web Service cho backend
- [ ] Set build/start command đúng
- [ ] Tạo PostgreSQL database
- [ ] Add `DATABASE_URL` vào backend env
- [ ] Verify backend URL: `/docs` hiển thị Swagger

### Frontend Deployment
- [ ] Tạo Web Service cho frontend
- [ ] Set `API_BASE_URL` = backend URL
- [ ] Verify frontend load được UI

### Integration
- [ ] Update `BACKEND_CORS_ORIGINS` với frontend URL
- [ ] Test tạo job từ frontend → lưu vào DB
- [ ] Test reload page → data vẫn còn

### Post-deployment
- [ ] Enable auto-deploy cho cả 2 services
- [ ] Setup UptimeRobot (optional)
- [ ] Document URLs trong README
- [ ] Share demo link với giảng viên

---

## 🌐 CUSTOM DOMAIN (OPTIONAL)

Render free tier hỗ trợ custom domain miễn phí.

**Bước:**
1. Mua domain (Namecheap, GoDaddy: ~$1/năm)
2. Render → Service → Tab "Settings" → "Custom Domain"
3. Add domain: `api.yourdomain.com` (backend)
4. Add domain: `app.yourdomain.com` (frontend)
5. Update DNS records theo hướng dẫn của Render

---

## 📊 OPTION A: HEROKU DEPLOYMENT

Nếu bạn chọn Heroku thay vì Render:

### Heroku vs Render

| Feature | Heroku | Render |
|---------|--------|--------|
| Free tier | ❌ Không còn (2022) | ✅ Có |
| Student pack | ✅ Free dyno + Postgres | ⚠️ Không có |
| Monorepo | ⚠️ Phức tạp (cần buildpack) | ✅ Native support |
| Sleep time | 30 phút | 15 phút |
| Cold start | 5-10s | 30-50s |
| Postgres | 10,000 rows (hobby) | 100MB storage |

### Heroku Setup (với Student Pack)

#### 1. Cài Heroku CLI

```bash
# Windows (PowerShell)
# Download: https://devcenter.heroku.com/articles/heroku-cli
# Hoặc dùng npm:
npm install -g heroku

# Verify
heroku --version
```

#### 2. Login Heroku

```bash
heroku login
# Press any key → browser login
```

#### 3. Deploy Backend

```bash
# Tạo app
heroku create job-tracker-backend-<your-name>

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini -a job-tracker-backend-<your-name>

# Set env vars
heroku config:set DEBUG=false -a job-tracker-backend-<your-name>
heroku config:set API_V1_PREFIX=/api/v1 -a job-tracker-backend-<your-name>

# Deploy
git push heroku main

# Init DB
heroku run python scripts/init_db_prod.py -a job-tracker-backend-<your-name>
```

#### 4. Tạo Procfile cho Backend

```bash
# Tạo file trong repo root
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

#### 5. Deploy Frontend lên Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Sign up với GitHub
3. Deploy từ repo:
   - Repository: `job-tracker-application`
   - Branch: `main`
   - Main file: `frontend/Home.py`
4. Set env:
   ```
   API_BASE_URL = https://job-tracker-backend-<your-name>.herokuapp.com
   ```

---

## 📚 TÀI LIỆU THAM KHẢO

- **Render Docs:** https://render.com/docs
- **Heroku Python:** https://devcenter.heroku.com/articles/getting-started-with-python
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

---

## 🎓 KẾT LUẬN

**Đề xuất cho đồ án tốt nghiệp:**

✅ **Render (Option B)** - Miễn phí, đơn giản, monorepo support tốt

**Lý do:**
- Setup nhanh (< 30 phút)
- Không cần credit card
- Auto deploy từ GitHub
- Free PostgreSQL + SSL/HTTPS
- Documentation tốt

**Lưu ý:**
- Cold start 30-50s → dùng UptimeRobot để giữ app awake
- Free tier đủ cho demo và bảo vệ đồ án
- Nếu cần production sau này → upgrade $7/month

---

**Good luck với đồ án! 🚀**

*Last updated: 2025-12-14*
