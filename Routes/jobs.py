from fastapi import APIRouter, Depends, HTTPException 
from typing import List
from dependencies.auth_dependency import get_current_user
from sqlalchemy.orm import Session 
from models.jobs import Jobs
from schemas.job import JobCreate,JobResponse,JobUpdate
from database.dependency import get_db

router = APIRouter(prefix="/jobs",tags=["Jobs"])

@router.post("/",response_model = JobResponse,status_code=201)

def create_jobs(job_data:JobCreate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):

    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403,detail="Only Recruiter Can Post Jobs")
    
    new_jobs = Jobs(
        title = job_data.title,
        description = job_data.description,
        company = job_data.company,
        location = job_data.location,
        salary = job_data.salary,
        experience_level = job_data.experience_level,
        skills = job_data.skills,
        recruiter_id = current_user.id
    )
    db.add(new_jobs)
    db.commit()
    db.refresh(new_jobs)
    return new_jobs 


@router.get("/",response_model = List[JobResponse]) 
def get_all_jobs(db:Session = Depends(get_db)):

    jobs = (db.query(Jobs).filter(Jobs.is_active == True).all()) 
    return jobs  


@router.get("/{id}",response_model = JobResponse)
def get_job_by_id(id:int,db:Session = Depends(get_db)):
    jobs = (db.query(Jobs).filter(Jobs.id == id,Jobs.is_active == True).first()) 
    if not jobs:
        raise HTTPException(status_code = 404,detail=f"Job With ID {id} not found")
    return jobs


@router.put("/{job_id}",response_model = JobResponse)
def update_jobs(job_id:int, job_data:JobUpdate,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403,detail = "Only Recruiter Can Update Jobs.")
    update_jobs = (db.query(Jobs).filter(Jobs.id == job_id,Jobs.is_active == True).first()) 
    if not update_jobs:
        raise HTTPException(status_code=404,detail= f"Job With ID {job_id} not found")
    if update_jobs.recruiter_id != current_user.id:
        raise HTTPException(status_code= 403,detail= "You are not authorised person to update the job details.")
    
    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(update_jobs, field, value)
    
    db.commit()
    db.refresh(update_jobs)
    return update_jobs 
    


@router.delete("/{job_id}") 
def delete_jobs(job_id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code = 403,detail = "Only Recruiter can Delete Jobs.")
    delete_job = (db.query(Jobs).filter(Jobs.id == job_id,Jobs.is_active == True).first()) 
    if not delete_job:
        raise HTTPException(status_code = 404,detail="Job Not Found") 
    if delete_job.recruiter_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "You are not authorised person to Delete the job details.")
    delete_job.is_active = False
    db.commit()
    return {"message": "Job Deleted Successfully"} 
 