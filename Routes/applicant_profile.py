from fastapi import APIRouter,Depends, HTTPException 
from sqlalchemy.orm import Session 
from dependencies.auth_dependency import get_current_user
from database.dependency import get_db
from models.applicant_profile import ApplicantProfile
from schemas.applicant_profile import (ApplicantProfileBase,ApplicantProfileCreate,
                                       UpdateApplicantProfile,ApplicantProfileResponse) 

router = APIRouter(prefix="/applicant-profile",tags=["Applicant Profile"])

@router.post("/",response_model = ApplicantProfileResponse,status_code = 201)

def create_applicant_profile(applicant_profile:ApplicantProfileCreate,db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    if current_user.role != "applicant":
        raise HTTPException(status_code = 403, detail = "only applicants can creat applicant profile.")

    existing_profile = (db.query(ApplicantProfile).filter(ApplicantProfile.user_id == current_user.id).first())
    if existing_profile:
        raise HTTPException(status_code = 404,detail = "applicant profile already exists.")
    
    new_profile = ApplicantProfile(user_id = current_user.id,**applicant_profile.model_dump()) 
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile 

@router.get("/",response_model = ApplicantProfileResponse)

def get_applicant_profile(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "applicant":
        raise HTTPException(status_code=403,detail="Only applicants can access applicant profiles.")
    profile = (db.query(ApplicantProfile).filter(ApplicantProfile.user_id == current_user.id).first())
    if not profile:
        raise HTTPException(status_code = 404, detail = "profile does not exists.")
    return profile

@router.patch("/",response_model = ApplicantProfileResponse)

def update_applicant_profile(update_profile:UpdateApplicantProfile,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "applicant":
        raise HTTPException(status_code = 403, detail ="Only applicants can update their profiles.")
    
    profile = (db.query(ApplicantProfile).filter(ApplicantProfile.user_id == current_user.id).first())
    if not profile:
        raise HTTPException(status_code = 400,detail = "profile does not exists.")
    update_data = update_profile.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(profile,field,value)
    db.commit()
    db.refresh(profile)
    return profile
     


