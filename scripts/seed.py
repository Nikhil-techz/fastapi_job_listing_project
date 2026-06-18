# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database.db import SessionLocal, engine, Base
# import database.base
# from models.user import Users
# from models.jobs import Jobs
# from models.application import Application
# import bcrypt

# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# def seed():
#     Base.metadata.create_all(bind=engine)
#     db = SessionLocal()

#     try:
#         # Seed users
#         users = [
#             Users(name="Alice Johnson", email="alice@example.com", password=hash_password("alice123")),
#             Users(name="Bob Smith",     email="bob@example.com",   password=hash_password("bob123")),
#             Users(name="Carol White",   email="carol@example.com", password=hash_password("carol123")),
#         ]
#         db.add_all(users)
#         db.flush()

#         # Seed jobs
#         jobs = [
#             Jobs(title="Backend Developer",    description="Build REST APIs using FastAPI and PostgreSQL.", company="TechCorp"),
#             Jobs(title="Frontend Developer",   description="Develop React-based UIs for web applications.",  company="WebWorks"),
#             Jobs(title="Data Analyst",         description="Analyse large datasets and build dashboards.",   company="DataHub"),
#             Jobs(title="DevOps Engineer",      description="Manage CI/CD pipelines and cloud infrastructure.", company="CloudBase"),
#             Jobs(title="Full Stack Developer", description="Work across backend and frontend systems.",       company="StartupXYZ"),
#         ]
#         db.add_all(jobs)
#         db.flush()

#         # Seed applications
#         applications = [
#             Application(user_id=users[0].id, job_id=jobs[0].id),
#             Application(user_id=users[0].id, job_id=jobs[2].id),
#             Application(user_id=users[1].id, job_id=jobs[1].id),
#             Application(user_id=users[2].id, job_id=jobs[3].id),
#             Application(user_id=users[2].id, job_id=jobs[4].id),
#         ]
#         db.add_all(applications)
#         db.commit()

#         print("Seeding complete.")
#         print(f"  Users       : {len(users)}")
#         print(f"  Jobs        : {len(jobs)}")
#         print(f"  Applications: {len(applications)}")

#     except Exception as e:
#         db.rollback()
#         print(f"Seeding failed: {e}")
#         raise
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed()