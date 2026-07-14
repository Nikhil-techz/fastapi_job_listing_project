from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from database.db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique= True, index=True, nullable=False)
    password = Column(String,nullable=False) 
    role = Column(String,nullable=False) 
    
    applications = relationship("Application",back_populates="user",cascade="all,delete")  

    job = relationship("Jobs",back_populates="recruiter",cascade="all, delete") 
    applicant_profile = relationship("ApplicantProfile",back_populates="user",uselist=False,cascade="all, delete-orphan",
)

    recruiter_profile = relationship("RecruiterProfile",back_populates="user",uselist=False,cascade="all, delete-orphan",)
    
    
    





