# Job Tracker Application - Project Structure

```
job-tracker-application/
│
├── backend/                          # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                       # FastAPI app entry point
│   │
│   ├── core/                         # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py                 # Environment configs
│   │   ├── database.py               # Database connection & session
│   │   └── security.py               # Security utilities (if needed)
│   │
│   ├── models/                       # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── job.py                    # Job model
│   │   ├── application.py            # Application model
│   │   ├── interview.py              # Interview model
│   │   ├── note.py                   # Note model
│   │   └── email_template.py         # EmailTemplate model
│   │
│   ├── schemas/                      # Pydantic schemas (validation)
│   │   ├── __init__.py
│   │   ├── job.py                    # Job request/response schemas
│   │   ├── application.py            # Application schemas
│   │   ├── interview.py              # Interview schemas
│   │   ├── note.py                   # Note schemas
│   │   ├── email_template.py         # EmailTemplate schemas
│   │   └── analytics.py              # Analytics response schemas
│   │
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── job_service.py            # Job CRUD + search/filter
│   │   ├── application_service.py    # Pipeline management
│   │   ├── interview_service.py      # Interview management
│   │   ├── note_service.py           # Note management
│   │   ├── email_service.py          # Email template management
│   │   └── analytics_service.py      # Analytics & reports
│   │
│   ├── api/                          # API endpoints (controllers)
│   │   ├── __init__.py
│   │   ├── deps.py                   # Dependencies (get_db, etc.)
│   │   └── v1/                       # API version 1
│   │       ├── __init__.py
│   │       ├── jobs.py               # /api/v1/jobs
│   │       ├── applications.py       # /api/v1/applications
│   │       ├── interviews.py         # /api/v1/interviews
│   │       ├── notes.py              # /api/v1/notes
│   │       ├── email_templates.py    # /api/v1/email-templates
│   │       └── analytics.py          # /api/v1/analytics
│   │
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py             # Custom validators
│   │   ├── formatters.py             # Data formatters
│   │   └── constants.py              # Constants (status enums, etc.)
│   │
│   └── tests/                        # Unit & integration tests
│       ├── __init__.py
│       ├── test_jobs.py
│       ├── test_applications.py
│       └── test_analytics.py
│
├── frontend/                         # Streamlit Frontend
│   ├── app.py                        # Main Streamlit app
│   │
│   ├── pages/                        # Multi-page app
│   │   ├── 1_🏠_Dashboard.py         # Dashboard overview
│   │   ├── 2_💼_Jobs.py              # Job management
│   │   ├── 3_📋_Applications.py      # Application pipeline
│   │   ├── 4_🎯_Interviews.py        # Interview schedule
│   │   ├── 5_📝_Notes.py             # Notes management
│   │   ├── 6_📧_Email_Templates.py   # Email templates
│   │   └── 7_📊_Analytics.py         # Reports & analytics
│   │
│   ├── components/                   # Reusable UI components
│   │   ├── __init__.py
│   │   ├── job_card.py               # Job display card
│   │   ├── pipeline_view.py          # Pipeline kanban view
│   │   ├── interview_calendar.py     # Calendar component
│   │   ├── filters.py                # Search/filter components
│   │   └── charts.py                 # Chart components
│   │
│   ├── services/                     # API client services
│   │   ├── __init__.py
│   │   ├── api_client.py             # Base API client (requests)
│   │   ├── job_service.py            # Job API calls
│   │   ├── application_service.py    # Application API calls
│   │   ├── interview_service.py      # Interview API calls
│   │   └── analytics_service.py      # Analytics API calls
│   │
│   ├── utils/                        # Frontend utilities
│   │   ├── __init__.py
│   │   ├── session_state.py          # Session state management
│   │   ├── formatters.py             # Display formatters
│   │   └── validators.py             # Input validators
│   │
│   └── config/                       # Frontend config
│       ├── __init__.py
│       └── settings.py               # API URL, constants
│
├── database/                         # Database files
│   ├── migrations/                   # Alembic migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   └── seeds/                        # Seed data
│       └── sample_data.sql
│
├── docs/                             # Documentation
│   ├── API.md                        # API documentation
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── CONTRIBUTING.md               # Contributing guidelines
│
├── scripts/                          # Utility scripts
│   ├── init_db.py                    # Initialize database
│   ├── seed_db.py                    # Seed sample data
│   └── run_dev.sh                    # Development runner
│
├── .env.example                      # Example environment variables
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── requirements-dev.txt              # Development dependencies
├── README.md                         # Project documentation
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker compose
└── database_design.md                # Database design (already created)
```

## Giải thích cấu trúc:

### Backend (FastAPI)
- **core/**: Cấu hình trung tâm (database, settings, security)
- **models/**: SQLAlchemy models map 1:1 với ERD
- **schemas/**: Pydantic schemas cho validation & serialization
- **services/**: Business logic tách biệt khỏi API layer
- **api/**: REST endpoints, routing, request handling
- **utils/**: Helper functions, constants, validators

### Frontend (Streamlit)
- **app.py**: Entry point, layout chính
- **pages/**: Multi-page app (7 pages cho 7 chức năng chính)
- **components/**: Reusable UI components
- **services/**: API client để gọi backend
- **utils/**: Frontend utilities (session, formatters)

### Database
- **migrations/**: Alembic cho version control CSDL
- **seeds/**: Sample data để test

### Docs & Scripts
- **docs/**: Tài liệu kỹ thuật
- **scripts/**: Automation scripts (init, seed, run)

## Mối liên kết Frontend ↔ Backend:

```
┌─────────────────────────────────────────────────────────┐
│                   STREAMLIT FRONTEND                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Pages     │→ │ Components  │→ │  Services   │    │
│  │ (UI Logic)  │  │ (Reusable)  │  │ (API Client)│    │
│  └─────────────┘  └─────────────┘  └──────┬──────┘    │
└─────────────────────────────────────────────┼──────────┘
                                              │
                                    HTTP REST API
                                    (JSON payload)
                                              │
┌─────────────────────────────────────────────┼──────────┐
│                   FASTAPI BACKEND           ▼          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │     API     │→ │  Services   │→ │   Models    │   │
│  │ (Endpoints) │  │ (Bus Logic) │  │ (SQLAlchemy)│   │
│  └─────────────┘  └─────────────┘  └──────┬──────┘   │
│         ↕               ↕                   ↕          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Schemas   │  │    Utils    │  │  Database   │   │
│  │  (Pydantic) │  │  (Helpers)  │  │   (SQLite)  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow Example (Tạo Job mới):
1. User nhập form trong `frontend/pages/2_💼_Jobs.py`
2. Frontend validate input bằng `utils/validators.py`
3. `frontend/services/job_service.py` gọi `POST /api/v1/jobs`
4. Backend `api/v1/jobs.py` nhận request
5. Validate với `schemas/job.py` (Pydantic)
6. `services/job_service.py` xử lý business logic
7. `models/job.py` (SQLAlchemy) insert vào database
8. Response trả về frontend qua JSON
9. Frontend update UI với data mới

## Tech Stack Summary:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.28+ | Interactive UI |
| Backend | FastAPI 0.104+ | REST API |
| ORM | SQLAlchemy 2.0+ | Database ORM |
| Validation | Pydantic 2.0+ | Data validation |
| Migration | Alembic | DB version control |
| Database (Dev) | SQLite | Local development |
| Database (Prod) | PostgreSQL | Production |
| HTTP Client | requests | API calls |
| Testing | pytest | Unit/integration tests |
