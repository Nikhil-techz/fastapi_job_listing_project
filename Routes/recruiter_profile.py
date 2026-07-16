from fastapi import APIRouter,Depends, HTTPException 
from sqlalchemy.orm import Session 
from dependencies.auth_dependency import get_current_user
from database.dependency import get_db
from models.recruiter_profile import RecruiterProfile
from schemas.recruiter_profile import(
    RecruiterProfileBase,
    RecruiterProfileCreate,
    RecruiterProfileUpdate,
    RecruiterProfileResponse
)

router = APIRouter(prefix="/recruiter-profile",tags=["Recruiter Profile"])

@router.post("/",response_model = RecruiterProfileResponse,status_code = 201)

def create_recruiter_profile(recruiter_profile:RecruiterProfileCreate,db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403,detail = "only recruiters can create recruiter profile.")
    existing_profile = (db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first())
    if existing_profile:
        raise HTTPException(status_code = 400, detail = "recruiter profile already exists.")
    new_profile = RecruiterProfile(user_id = current_user.id, **recruiter_profile.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile 

@router.get("/",response_model = RecruiterProfileResponse)
def get_recruiter_profile(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403,detail="Only recruiters can access recruiter profiles.")
    profile = (db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first())
    if not profile:
        raise HTTPException(status_code = 404, detail = "profile does not exists.")
    return profile

@router.patch("/",response_model = RecruiterProfileResponse)

def update_applicant_profile(update_profile:RecruiterProfileUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403, detail ="Only applicants can update their profiles.")
    
    profile = (db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first())
    if not profile:
        raise HTTPException(status_code = 400,detail = "profile does not exists.")
    update_data = update_profile.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(profile,field,value)
    db.commit()
    db.refresh(profile)
    return profile 
