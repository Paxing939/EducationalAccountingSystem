from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schemas.students import *
from models.students import *
import requests

db_name = 'students_db'
db_user = 'user'
db_pass = 'password'
db_host = 'postgres_db'
db_port = '5432'

# Connect to the database
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def authenticate_user(username: str, password: str):
    auth_service_url = "http://auth_service:8002/login"
    auth_payload = {
        "username": username,
        "password": password
    }
    auth_headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(auth_service_url, json=auth_payload, headers=auth_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")


@app.post("/students/create")
def create_student(student: StudentCreate):
    db = SessionLocal()
    if db.query(EducationType).filter(EducationType.id == student.education_type_id).first() is None:
        raise HTTPException(status_code=400, detail="Invalid education type id")
    if db.query(Education).filter(Education.id == student.education_id).first() is None:
        raise HTTPException(status_code=400, detail="Invalid education id")
    student.payments = [payment.model_dump(mode='json') for payment in student.payments]
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/edit")
def edit_student(student: StudentUpdate):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.id == student.id).first()
    if db_student is None:
        raise HTTPException(status_code=400, detail="Student not found")
    if student.group:
        db_student.group = student.group
    if student.full_name:
        db_student.full_name = student.full_name
    if student.term:
        db_student.term = student.term
    if student.start_date:
        db_student.start_date = student.start_date
    if student.profession:
        db_student.profession = student.profession
    if student.degree:
        db_student.degree = student.degree
    if student.education_type_id:
        if db.query(EducationType).filter(EducationType.id == student.education_type_id).first() is None:
            raise HTTPException(status_code=400, detail="Invalid education type id")
        db_student.education_type_id = student.education_type_id
    if student.login:
        db_student.login = student.login
    if student.birth_date:
        db_student.birth_date = student.birth_date
    if student.education_id:
        if db.query(Education).filter(Education.id == student.education_id).first() is None:
            raise HTTPException(status_code=400, detail="Invalid education id")
        db_student.education_id = student.education_id
    if student.payment:
        db_student.payment = student.payment
    if student.protocol_number:
        db_student.protocol_number = student.protocol_number
    if student.full_name_bel:
        db_student.full_name_bel = student.full_name_bel
    if student.profession_bel:
        db_student.profession_bel = student.profession_bel
    db_student.referrer_organization = student.referrer_organization
    db_student.theory_end_date = student.theory_end_date
    db_student.practice_start_date = student.practice_start_date
    db_student.practice_end_date = student.practice_end_date
    db_student.end_date = student.end_date
    db_student.exam_date = student.exam_date
    db_student.email = student.email
    db_student.previous_profession = student.previous_profession
    db_student.organization = student.organization
    db_student.certificate_number = student.certificate_number
    db_student.grad_id = student.grad_id
    db_student.practice_organization = student.practice_organization
    db_student.graduation_date = student.graduation_date
    db_student.grade_1 = student.grade_1
    db_student.grade_2 = student.grade_2
    db_student.payments = [payment.model_dump(mode='json') for payment in student.payments]
    db_student.theory_hours = student.theory_hours
    db_student.practice_hours = student.practice_hours
    db_student.status = student.status
    db_student.comments = student.comments
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students")
def get_students():
    db = SessionLocal()
    students = db.query(Student).all()
    return students
