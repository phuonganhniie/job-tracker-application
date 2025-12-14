"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import init_db
from backend.api.v1 import jobs, analytics, interviews

# Import all models to ensure relationships are registered
import backend.models  # noqa: F401

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST API for Job Tracker Application",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(interviews.router, prefix=settings.API_V1_PREFIX)

# TODO: Add other routers (applications, notes, email_templates)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    
    # Auto-seed database if empty (first-time setup)
    try:
        from backend.core.database import SessionLocal
        from backend.models.job import Job
        import os
        
        db = SessionLocal()
        job_count = db.query(Job).count()
        db.close()
        
        # Only seed if database is empty AND AUTO_SEED is enabled
        auto_seed = os.getenv("AUTO_SEED_DB", "false").lower() == "true"
        
        if job_count == 0 and auto_seed:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("🌱 Database is empty, running auto-seed...")
            
            import subprocess
            import sys
            result = subprocess.run(
                [sys.executable, "scripts/seed_db_prod.py"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✅ Auto-seed completed successfully")
            else:
                logger.warning(f"⚠️ Auto-seed failed: {result.stderr}")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"⚠️ Auto-seed check failed: {e}")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Job Tracker API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
