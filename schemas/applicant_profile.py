from pydantic import BaseModel
from typing import Optional
class ApplicantProfileBase(BaseModel):
    full_name:str
    contact = str
    location = Optional[str] = None
    experience = Optional[str] = None
    education =Optional[str] = None
    linkedin = Optional[str] = None
    github =  Optional[str] = None
    profile_picture = Optional[str] = None 

class ApplicantProfileCreate(ApplicantProfileBase):
    pass


class UpdateApplicantProfile(BaseModel):
    full_name = Optional[str] = None
    contact = Optional[str] = None
    location = Optional[str] = None
    experience = Optional[str] = None
    education = Optional[str] = None
    linkedin = Optional[str] = None
    github =  Optional[str] = None
    profile_picture = Optional[str] = None 

class ApplicantProfileResponse(ApplicantProfileBase):
    id: int

    model_config = {
        "from_attributes": True
    }