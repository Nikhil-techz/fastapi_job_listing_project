from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.dependency import get_db
from models.user import Users
from config.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)):
    
    payload = verify_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401,detail="invalid token")

    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401,detail="user not found")

    return user 
        
    