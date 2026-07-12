from fastapi import APIRouter,Depends, HTTPException 
from sqlalchemy.orm import Session 
from models.application import Application
from models.jobs import Jobs
from models.user import Users
from schemas.application import (
    ApplicationStatus,
    ApplicationBase,
    ApplicationCreate,
    ApplicationResponse,
    MyApplicationResponse,
    RecruiterApplicationResponse,
    UpdateApplicationStatus,
) 

from dependencies.auth_dependency import get_current_user
from database.dependency import get_db


router = APIRouter(prefix="/Applications",tags=["Applications"])

@router.post("/",response_model= ApplicationResponse,status_code = 201)

def create_application(
    application_create: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "applicant":
        raise HTTPException(status_code = 403, detail = "only applicants can apply for job")
    existing_job = (db.query(Jobs).filter(Jobs.id == application_create.job_id).first()) 
    if not existing_job:
        raise HTTPException(status_code=404,detail=f"Job with id {application_create.job_id} not found")
    existing_application = (db.query(Application).filter(Application.applicant_id == current_user.id,
                                                         Application.job_id == application_create.job_id).first()) 
    if existing_application:
        raise HTTPException(status_code = 409, detail = "You have already applied for this job")
    
    new_application = Application(
        applicant_id = current_user.id,
        job_id =      application_create.job_id,
        status =      ApplicationStatus.APPLIED
         
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application 


@router.get("/my-applications",response_model = list[ApplicationResponse])

def get_my_applications(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if not current_user.role != "applicant":
        raise HTTPException(status_code = 403,detail = "Only applicants can view their applications")
    applications = (db.query(Application).filter(Application.applicant_id == current_user.id).all()) 
    
    return applications 



@router.get("/jobs/{job_id}/applications",response_model = list[RecruiterApplicationResponse]) 

def get_job_applications(job_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403, detail = "only recruiter can see the job applications")

    job =(db.query(Jobs).filter(Jobs.id == job_id).first()) 
    if not job:
        raise HTTPException(status_code = 404, detail = "Jobs with id {job_id} not exists.")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code = 403,detail = "You are not authorized to view applications for this job.")
    job_applications = (db.query(Application).filter(Application.job_id == job_id).all()) 
    response = []
    for application in job_applications:
        response.append(
            RecruiterApplicationResponse(
                application_id = application.id,
                applicant_id = application.applicant_id,
                applicant_name = application.user.name,
                applicant_email = application.user.email,
                status = application.status,
                applied_at = application.applied_at
            )
        )
    return response 


@router.patch("/application/{application_id}",response_model = ApplicationResponse) 

def update_application(application_id:int,application_update:UpdateApplicationStatus,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403, detail = "You are not authorized to update the application.") 
    application = (db.query(Application).filter(Application.id == application_id).first())
    if not application:
        raise HTTPException(status_code = 404, detail = "Application with id {application_id} does not exists.") 
    job = (db.query(Jobs).filter(Jobs.id == application.job_id).first()) 
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You are not authorized to update this application.") 
    application.status = application_update.status 
    db.commit()
    db.refresh(application)
    return application 
  
@router.patch("/application/{application_id}/withdraw") 

def withdraw_application(application_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "applicant":
        raise HTTPException(status_code = 403,detail = "Only Applicants can withdrawn the applications.")
    application = (db.query(Application).filter(Application.id == application_id).first())
    if not application:
        raise HTTPException(status_code = 404, detail = f"Application with {application_id} does not exists.")

    if application.applicant_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You are not authorized to withdraw this application.")

    if application.status == ApplicationStatus.WITHDRAWN:
        raise HTTPException(status_code = 409,detail="Application has already been withdrawn.")
    if application.status == ApplicationStatus.APPLIED:
        application.status = ApplicationStatus.WITHDRAWN
        db.commit()
        db.refresh(application)
        return application 
    raise HTTPException(status_code=400,detail="Application cannot be withdrawn after the review process has started.")  
