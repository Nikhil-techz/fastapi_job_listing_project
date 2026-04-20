from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from database.db import Base

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String,nullable=False)
    description = Column(String)
    company = Column(String,nullable=False)
    
    applications = relationship("Application",back_populates="job",cascade="all,delete") 

