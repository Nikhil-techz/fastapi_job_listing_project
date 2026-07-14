from pydantic import BaseModel
from typing import Optional

class RecruiterProfileBase(BaseModel):
    company_name: str
    designation: str
    phone: str
    company_website: Optional[str] = None
    company_logo: Optional[str] = None


class RecruiterProfileCreate(RecruiterProfileBase):
    pass


class RecruiterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    company_website: Optional[str] = None
    company_logo: Optional[str] = None


class RecruiterProfileResponse(RecruiterProfileBase):
    id: int

    model_config = {
        "from_attributes": True
    }    