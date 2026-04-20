from pydantic import BaseModel
from schemas.job import JobResponse
from schemas.user import UserResponse


class ApplicationBase(BaseModel):
    user_id: int
    job_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: int
    user: UserResponse
    job: JobResponse

    model_config = {"from_attributes": True}
