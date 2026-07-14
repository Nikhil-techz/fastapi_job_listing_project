from fastapi import APIRouter, Depends, HTTPException 
# from fastapi.security import OAuth2PasswordRequestForm
from config.security import create_access_token 
from dependencies.auth_dependency import get_current_user
from sqlalchemy.orm import Session
from models.user import Users
from schemas.user import UserLogin
from config.security import verify_password
from database.dependency import get_db

router = APIRouter()


@router.post("/login")
def login(login_data:UserLogin,db:Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == login_data.email).first()
    if user is None:
        raise HTTPException(status_code=401,detail = "Invalid Credentials")
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    token = create_access_token(data={
        "sub": str(user.id),
        "role": user.role
        }) 
    
    return  { 
        "access_token":token ,
        "token_type":  "bearer"
    }

    
@router.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email,
        "role":current_user.role
    }


     
