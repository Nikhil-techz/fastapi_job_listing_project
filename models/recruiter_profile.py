from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class RecruiterProfile(Base):
    __tablename__ = "recruiter_profile"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column( Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    company_name = Column(String(150), nullable=False)
    designation = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    company_website = Column(String, nullable=True)
    company_logo = Column(String, nullable=True)

    user = relationship("Users",back_populates="recruiter_profile")  