from fastapi import FastAPI
from database.db import engine, Base
import database.base 


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Job listing app is running "} 