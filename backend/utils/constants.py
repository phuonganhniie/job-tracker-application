"""
Constants and enums used throughout the application
"""
from enum import Enum


class JobStatus(str, Enum):
    """Job application status enum"""
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    HIRED = "Hired"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class WorkType(str, Enum):
    """Work type enum"""
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ONSITE = "Onsite"


class InterviewType(str, Enum):
    """Interview type enum"""
    PHONE_SCREENING = "Phone Screening"
    VIDEO_CALL = "Video Call"
    TECHNICAL_TEST = "Technical Test"
    ONSITE_INTERVIEW = "Onsite Interview"
    FINAL_ROUND = "Final Round"
    HR_INTERVIEW = "HR Interview"


class InterviewResult(str, Enum):
    """Interview result enum"""
    PASSED = "Passed"
    FAILED = "Failed"
    PENDING = "Pending"


class NoteType(str, Enum):
    """Note type enum"""
    GENERAL = "General"
    RESEARCH = "Research"
    PREPARATION = "Preparation"
    INTERVIEW_FEEDBACK = "Interview_Feedback"
    FOLLOW_UP = "Follow_Up"
    REMINDER = "Reminder"


class Priority(str, Enum):
    """Priority level enum"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class EmailTemplateType(str, Enum):
    """Email template type enum"""
    THANK_YOU = "Thank_You"
    FOLLOW_UP = "Follow_Up"
    WITHDRAW = "Withdraw"
    ACCEPT_OFFER = "Accept_Offer"
    DECLINE_OFFER = "Decline_Offer"
    REQUEST_INFO = "Request_Info"


class JobSource(str, Enum):
    """Common job sources"""
    LINKEDIN = "LinkedIn"
    INDEED = "Indeed"
    TOPCV = "TopCV"
    VIETNAMWORKS = "VietnamWorks"
    COMPANY_WEBSITE = "Company Website"
    REFERRAL = "Referral"
    RECRUITER = "Recruiter"
    OTHER = "Other"


# Pipeline status order (for analytics)
PIPELINE_ORDER = [
    JobStatus.APPLIED,
    JobStatus.SCREENING,
    JobStatus.INTERVIEW,
    JobStatus.OFFER,
    JobStatus.HIRED,
]

# Currency options
CURRENCIES = ["VND", "USD", "EUR", "GBP", "SGD"]
