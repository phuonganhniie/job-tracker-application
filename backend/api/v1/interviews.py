"""
Interviews API Router - CRUD endpoints for interview management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from backend.api.deps import get_db
from backend.services.interview_service import InterviewService
from backend.schemas.interview import (
    InterviewCreate,
    InterviewUpdate,
    InterviewResponse,
    InterviewListResponse,
    InterviewFilter
)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/", response_model=InterviewResponse, status_code=201)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new interview
    
    - **job_id**: ID of the job this interview belongs to (required)
    - **round_number**: Interview round number (required, >= 1)
    - **scheduled_date**: Date and time of the interview (required)
    - **interview_type**: Type of interview (Phone Screening, Video Call, Technical Test, Onsite Interview, Final Round, HR Interview)
    - **location**: Physical location or meeting room
    - **meeting_link**: Video call link if applicable
    - **interviewer_name**: Name of the interviewer(s)
    - **interviewer_title**: Title/role of the interviewer(s)
    - **preparation_notes**: Notes for interview preparation
    """
    try:
        interview = InterviewService.create_interview(db, interview_data)
        return interview
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create interview: {str(e)}")


@router.get("/", response_model=InterviewListResponse)
def get_interviews(
    job_id: Optional[int] = Query(None, description="Filter by job ID"),
    interview_type: Optional[str] = Query(None, description="Filter by interview type"),
    result: Optional[str] = Query(None, description="Filter by result (Passed, Failed, Pending)"),
    scheduled_date_from: Optional[datetime] = Query(None, description="Filter from date"),
    scheduled_date_to: Optional[datetime] = Query(None, description="Filter to date"),
    db: Session = Depends(get_db)
):
    """
    Get all interviews with optional filtering
    
    Returns list of interviews with total count
    """
    filters = InterviewFilter(
        job_id=job_id,
        interview_type=interview_type,
        result=result,
        scheduled_date_from=scheduled_date_from,
        scheduled_date_to=scheduled_date_to
    )
    
    interviews, total = InterviewService.get_interviews(db, filters)
    
    return InterviewListResponse(
        items=interviews,
        total=total
    )


@router.get("/upcoming", response_model=InterviewListResponse)
def get_upcoming_interviews(
    days: int = Query(7, description="Number of days to look ahead", ge=1, le=30),
    db: Session = Depends(get_db)
):
    """
    Get upcoming interviews within specified days
    
    - **days**: Number of days to look ahead (default: 7, max: 30)
    """
    interviews = InterviewService.get_upcoming_interviews(db, days)
    
    return InterviewListResponse(
        items=interviews,
        total=len(interviews)
    )


@router.get("/job/{job_id}", response_model=InterviewListResponse)
def get_interviews_by_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all interviews for a specific job
    
    Returns interviews ordered by round number
    """
    interviews = InterviewService.get_interviews_by_job(db, job_id)
    
    return InterviewListResponse(
        items=interviews,
        total=len(interviews)
    )


@router.get("/stats")
def get_interview_stats(
    job_id: Optional[int] = Query(None, description="Get stats for specific job"),
    db: Session = Depends(get_db)
):
    """
    Get interview statistics
    
    Returns:
    - total: Total number of interviews
    - passed: Number of passed interviews
    - failed: Number of failed interviews
    - pending: Number of pending interviews
    - pass_rate: Pass rate percentage
    - by_type: Count by interview type
    """
    return InterviewService.get_interview_stats(db, job_id)


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Get interview by ID
    """
    interview = InterviewService.get_interview_by_id(db, interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview with id {interview_id} not found")
    
    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an interview
    
    All fields are optional - only provided fields will be updated
    """
    interview = InterviewService.update_interview(db, interview_id, interview_data)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview with id {interview_id} not found")
    
    return interview


@router.patch("/{interview_id}/result", response_model=InterviewResponse)
def update_interview_result(
    interview_id: int,
    result: str = Query(..., description="Interview result: Passed, Failed, or Pending"),
    feedback: Optional[str] = Query(None, description="Feedback from the interview"),
    db: Session = Depends(get_db)
):
    """
    Update interview result and feedback
    
    - **result**: Passed, Failed, or Pending (required)
    - **feedback**: Optional feedback notes
    """
    if result not in ["Passed", "Failed", "Pending"]:
        raise HTTPException(
            status_code=400, 
            detail="Result must be one of: Passed, Failed, Pending"
        )
    
    interview = InterviewService.update_interview_result(db, interview_id, result, feedback)
    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview with id {interview_id} not found")
    
    return interview


@router.delete("/{interview_id}", status_code=204)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an interview
    
    Returns 204 No Content on success
    """
    success = InterviewService.delete_interview(db, interview_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Interview with id {interview_id} not found")
    
    return None
