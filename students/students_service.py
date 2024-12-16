from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import requests

db_name = 'students_db'
db_user = 'user'
db_pass = 'password'
db_host = 'postgres_db'
db_port = '5432'

# Connect to the database
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    # profession_id = Column(Integer)


Base.metadata.create_all(bind=engine)


class StudentCreate(BaseModel):
    name: str
    age: int
    education_type: int
    # profession_id: int
token = ""

def authenticate_user(username: str, password: str):
    auth_service_url = "http://auth_service:8002/login"
    auth_payload = {
        "username": username,
        "password": password
    }
    auth_headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(auth_service_url, json = auth_payload, headers=auth_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

@app.post("/students/")
def create_student(student: StudentCreate):
    db = SessionLocal()
    db_student = Student(name=student.name, age=student.age)  # , profession_id=student.profession_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
