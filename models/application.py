from sqlalchemy import Column, Integer, ForeignKey,DateTime,Enum
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime
from schemas.application import ApplicationStatus

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    applicant_id  = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))  
    status = Column(Enum(ApplicationStatus),nullable = False )
    applied_at = Column(DateTime,default = datetime.utcnow) 
    
    user = relationship("Users",back_populates="applications")
    job = relationship("Jobs",back_populates="applications") 
    


    
