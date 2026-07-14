from datetime import datetime
from enum import Enum
from pydantic import BaseModel 




class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    UNDER_REVIEW = "Under Review"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"
    HIRED = "Hired"
    WITHDRAWN = "Withdrawn"

class ApplicationBase(BaseModel):
    job_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: int
    applicant_id: int
    status: ApplicationStatus
    applied_at: datetime
    

    model_config = {"from_attributes": True} 




class MyApplicationResponse(BaseModel):
    application_id: int
    job_title: str
    company: str
    location: str
    status: ApplicationStatus
    applied_at: datetime

    model_config = {
        "from_attributes": True
    }


class RecruiterApplicationResponse(BaseModel):
    application_id: int
    applicant_id: int
    applicant_name: str
    applicant_email: str
    status: ApplicationStatus
    applied_at: datetime

    model_config = {
        "from_attributes": True
    }
 


class UpdateApplicationStatus(BaseModel):
    status: ApplicationStatus