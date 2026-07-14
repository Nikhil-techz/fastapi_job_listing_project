from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database.db import Base
from models.user import Users 

class ApplicantProfile(Base):
    __tablename__ = "applicant_profile"

    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False, unique = True)
    full_name = Column(String(100),nullable = False)
    contact = Column(String(15),nullable = False)
    location = Column(String(100),nullable = True)
    experience = Column(String,nullable = True)
    education = Column(String,nullable = True)
    linkedin = Column(String)
    github = Column(String)
    profile_picture = Column(String, nullable=True) 

    user = relationship("Users", back_populates="applicant_profile") 





