from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional 

class UserRole(str,Enum):
    applicant = "applicant"
    recruiter = "recruiter"
    
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role:UserRole 


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    


class UserResponse(UserBase):
    id: int
    role:UserRole

    model_config = {"from_attributes": True} 


class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str 
    
    
