from sqlalchemy import Column, Integer,String, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String,nullable=False)
    description = Column(String)
    company = Column(String,nullable=False)
    location = Column(String,nullable=False)
    salary = Column(String,nullable=False)
    experience_level = Column(String,nullable=False)
    skills = Column(String,nullable= False)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime,default = datetime.utcnow)
    recruiter_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    is_featured = Column(Boolean, default=False)
    featured_until = Column(DateTime, nullable=True)
    featured_priority = Column(Integer, default=0)
    
    applications = relationship("Application",back_populates="job",cascade="all,delete") 
    recruiter = relationship("Users",back_populates = "job")
