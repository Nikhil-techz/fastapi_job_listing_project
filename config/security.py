from fastapi import HTTPException,status
from passlib.context import CryptContext 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.settings import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
    
def create_access_token(data:dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp":expire})
    
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return encoded_jwt   

def verify_token(token:str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms = settings.ALGORITHM
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code = 401,
            detail= "Invalid Token"

        )

