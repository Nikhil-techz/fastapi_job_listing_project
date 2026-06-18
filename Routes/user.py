from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from models.user import Users 
from schemas.user import UserCreate
from config.security import hash_password 
from database.dependency import get_db

router = APIRouter()

@router.post("/register")
def register(user_data:UserCreate, db:Session = Depends(get_db)):
    print("Received role:", user_data.role)
    existing_user = db.query(Users).filter(Users.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code= 400,detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    new_user_created = Users(
        name = user_data.name,
        email = user_data.email,
        password = hashed_password,
        role = user_data.role
    )

    db.add(new_user_created)
    db.commit()
    db.refresh(new_user_created)
    return {"message":"User Registered Successfully"} 
