from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))  
    
    user = relationship("Users",back_populates="applications")
    job = relationship("Jobs",back_populates="applications") 


    
