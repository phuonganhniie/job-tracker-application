# 💼 Job Tracker Application

Ứng dụng fullstack giúp quản lý quá trình ứng tuyển việc làm một cách có hệ thống và hiệu quả.

## 📋 Giới thiệu

Job Tracker là giải pháp toàn diện cho việc theo dõi các đơn ứng tuyển, từ giai đoạn nộp hồ sơ đến khi nhận offer. Ứng dụng giúp bạn:

- ✅ Quản lý thông tin các công việc đã/đang ứng tuyển
- 📊 Theo dõi trạng thái pipeline (Applied → Screening → Interview → Offer → Hired)
- 🎯 Quản lý lịch phỏng vấn chi tiết
- 📝 Ghi chú quan trọng cho từng job và interview
- 📧 Lưu trữ mẫu email để follow-up
- 📈 Báo cáo và thống kê trực quan

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────┐
│    Frontend (Streamlit)                 │
│    - Multi-page app                     │
│    - Interactive UI                     │
│    - Charts & Analytics                 │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API (JSON)
┌──────────────┴──────────────────────────┐
│    Backend (FastAPI)                    │
│    - RESTful API                        │
│    - Business Logic                     │
│    - Auto-generated Docs                │
└──────────────┬──────────────────────────┘
               │ SQLAlchemy ORM
┌──────────────┴──────────────────────────┐
│    Database (SQLite/PostgreSQL)         │
│    - 5 tables (ERD design)              │
└─────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.0+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Migration**: Alembic

### Frontend

- **Framework**: Streamlit 1.28+
- **HTTP Client**: requests
- **Data Processing**: pandas
- **Charts**: Built-in Streamlit charts

### DevOps

- **Testing**: pytest
- **Code Quality**: black, flake8, mypy
- **Containerization**: Docker (optional)

## 🚀 Cài đặt và chạy

## ⚡ Quick Start (TL;DR)

> **⚠️ Yêu cầu:** Python 3.11+ (khuyến nghị Python 3.11 để đảm bảo ổn định khi cài đặt dependencies)

**Khuyến nghị thêm:**

- Node.js >= 18
- npm hoặc yarn
- Git

### 1. Clone repository

```bash
git clone <repository-url>
cd job-tracker-application
```

### 2. Cài đặt dependencies

#### 🍎 macOS / Linux

```bash
# Kiểm tra phiên bản Python (cần 3.11+)
python3 --version

# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt
```

#### 🪟 Windows

##### Option 1: PowerShell

```powershell
# Kiểm tra phiên bản Python (cần 3.11+)
python --version

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1

# Nếu gặp lỗi ExecutionPolicy, chạy lệnh sau (chỉ cần 1 lần):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Cài đặt packages
pip install -r requirements.txt
```

##### Option 2: Git Bash

```bash
# Kiểm tra phiên bản Python (cần 3.11+)
python --version

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
source venv/Scripts/activate

# Cài đặt packages
pip install -r requirements.txt
```

### 3. Cấu hình environment

#### macOS / Linux:

```bash
# Copy file .env.example thành .env
cp .env.example .env

# Chỉnh sửa .env nếu cần (mặc định dùng SQLite)
nano .env  # hoặc vim, code, etc.
```

#### Windows (PowerShell):

```powershell
# Copy file .env.example thành .env
Copy-Item .env.example .env

# Chỉnh sửa .env nếu cần
notepad .env  # hoặc code .env
```

#### Windows (Git Bash):

```bash
# Copy file .env.example thành .env
cp .env.example .env

# Chỉnh sửa .env nếu cần
notepad .env  # hoặc vim, code .env
```

### 4. Khởi tạo database

#### macOS / Linux:

```bash
# Tạo database và tables
python scripts/init_db.py

# (Optional) Seed dữ liệu mẫu
python scripts/seed_db.py
```

#### Windows (PowerShell):

```powershell
# Tạo database và tables
.\venv\Scripts\python.exe scripts/init_db.py

# (Optional) Seed dữ liệu mẫu
.\venv\Scripts\python.exe scripts/seed_db.py
```

#### Windows (Git Bash):

```bash
# Tạo database và tables
python scripts/init_db.py

# (Optional) Seed dữ liệu mẫu
python scripts/seed_db.py
```

### 5. Chạy Backend API

#### macOS / Linux:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Windows (PowerShell):

```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Windows (Git Bash):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: `http://localhost:8000`

- API Docs (Swagger): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 6. Chạy Frontend (Mở terminal mới)

#### macOS / Linux:

```bash
# Đảm bảo venv đã được kích hoạt
source venv/bin/activate

# Chạy Streamlit
streamlit run frontend/Home.py
```

#### Windows (PowerShell):

```powershell
# Đảm bảo venv đã được kích hoạt
.\venv\Scripts\Activate.ps1

# Chạy Streamlit
.\venv\Scripts\python.exe -m streamlit run frontend/Home.py
```

#### Windows (Git Bash):

```bash
# Đảm bảo venv đã được kích hoạt
source venv/Scripts/activate

# Chạy Streamlit
streamlit run frontend/Home.py
```

Frontend sẽ chạy tại: `http://localhost:8501`

### 🔧 Troubleshooting

#### Python không tìm thấy hoặc sai phiên bản

- **macOS/Linux**: Thử `python3.11 --version` hoặc cài Python 3.11 từ [python.org](https://www.python.org/downloads/)
- **Windows**: Tải Python 3.11 từ [python.org](https://www.python.org/downloads/windows/) và đảm bảo chọn "Add Python to PATH" khi cài đặt

#### PowerShell ExecutionPolicy Error

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Module not found errors

```bash
# Đảm bảo virtual environment đã được kích hoạt và cài lại dependencies
pip install -r requirements.txt
```

#### Port đã được sử dụng

- Đổi port khác: `--port 8001` cho backend hoặc `--server.port 8502` cho frontend

## 🧪 Testing

```powershell
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=backend tests/
```

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team Members

- **Backend Developer**: Phuong Anh, Duc Minh, Hoang Duy
- **Frontend Developer**: Gia Hoa, Kieu An

## 🎯 Roadmap

### Phase 1 ✅ (Completed)

- [x] Database design & ERD
- [x] Backend API (Jobs, Analytics)
- [x] Frontend (Dashboard, Jobs Management)
- [x] Basic CRUD operations for Jobs

### Phase 2 🚧 (Current)

**Focus: Core features completion**

- [ ] Frontend: Edit & Delete UI for Jobs
- [ ] Backend API: Interviews CRUD
- [ ] Frontend: Interviews Management Page
- [ ] Backend API: Email Templates CRUD
- [ ] Frontend: Email Templates Management Page

**Out of scope for Phase 2:**

- ❌ Applications API (status already tracked in Job model)
- ❌ Notes API (moved to Phase 3)
- ❌ Email sending functionality (moved to Phase 3)

### Phase 3 📅 (Future enhancements)

**Advanced Features:**

- [ ] Notes system (API + UI for job/interview notes)
- [ ] Email integration (send emails from templates)
- [ ] Advanced analytics & reports
- [ ] Export reports (PDF, Excel)

**Enterprise Features:**

- [ ] User authentication & authorization
- [ ] Multi-user support
- [ ] Calendar integration (Google Calendar)
- [ ] Mobile responsive UI
- [ ] Notification system
- [ ] AI-powered insights & recommendations

## 🐛 Known Issues

- Email templates chưa có chức năng gửi email tự động
- Timeline analytics đang dùng query đơn giản, cần tối ưu với database-specific functions
- Note validation (at least one of job_id or interview_id) cần thêm CHECK constraint ở DB level

## 💡 Tips

- Sử dụng API docs tại `/docs` để test endpoints
- Check backend logs nếu frontend không load được data
- Dùng `seed_db.py` để tạo sample data cho development
- Enable SQLAlchemy echo trong config để debug SQL queries

---

**Built with ❤️ by Team 13 - UIT CN1.K2025 - Lap Trinh Python**

## 👨‍💻 Contributor Note

Một số cải thiện nhỏ về tài liệu đã được thêm vào
nhằm giúp project dễ đọc và dễ tiếp cận hơn cho người mới.
