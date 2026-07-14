from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from Routes import user,auth,jobs,application
import database.base 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(user.router,prefix="/users",tags=["Users"])
app.include_router(auth.router,prefix="/auth",tags=["Auth"]) 
app.include_router(jobs.router)
app.include_router(application.router) 

@app.get("/")
def home():
    return {"message": "Job listing app is running "} 


