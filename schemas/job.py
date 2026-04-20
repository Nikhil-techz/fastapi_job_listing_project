from pydantic import BaseModel
from typing import Optional


class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    company: str


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None


class JobResponse(JobBase):
    id: int

    model_config = {"from_attributes": True}  
