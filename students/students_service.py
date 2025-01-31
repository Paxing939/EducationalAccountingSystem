from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
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

class EducationType(Base):
    __tablename__ = "education_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))

class Education(Base):
    __tablename__ = "educations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    referrer_organization = Column(String(256), nullable=True)
    group = Column(String(10))
    full_name = Column(String(128))
    term = Column(Float)
    start_date = Column(Date)
    theory_end_date = Column(Date, nullable=True)
    practice_start_date = Column(Date, nullable=True)
    practice_end_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    exam_date = Column(Date, nullable=True)
    profession = Column(String(256))
    category = Column(Integer)
    education_type_id = Column(Integer, ForeignKey(EducationType.id))
    login = Column(String(128))
    email = Column(String(128), nullable=True)
    birth_date = Column(Date)
    education_id = Column(Integer, ForeignKey(Education.id))
    previous_profession = Column(String(256), nullable=True)
    payment = Column(Float)
    organization = Column(String(256), nullable=True)
    protocol_number = Column(String(20))
    certificate_number = Column(String(20), nullable=True)
    grad_id = Column(Integer, nullable=True)
    theory_hours = Column(Integer, default=0)
    practice_hours = Column(Integer, default=0)
    practice_organization = Column(String(256), nullable=True)
    status = Column(Integer, default=0)
    payments = Column(ARRAY(JSONB), default=[])
    comments = Column(String(256), default='')
    graduation_date = Column(Date, nullable=True)
    grade_1 = Column(Integer, nullable=True)
    grade_2 = Column(Integer, nullable=True)
    full_name_bel = Column(String(128))
    profession_bel = Column(String(256))


Base.metadata.create_all(bind=engine)

class StudentPayment(BaseModel):
    date: date
    amount: float

class StudentBase(BaseModel):
    referrer_organization: str | None = None
    theory_end_date: date | None = None
    practice_start_date: date | None = None
    practice_end_date: date | None = None
    end_date: date | None = None
    exam_date: date | None = None
    email: str | None = None
    previous_profession: str | None = None
    organization: str | None = None
    certificate_number: str | None = None
    grad_id: int | None = None
    practice_organization: str | None = None
    graduation_date: date | None = None
    grade_1: int | None = None
    grade_2: int | None = None
    payments: list[StudentPayment] = []
    theory_hours: int = 0
    practice_hours: int = 0
    status: int = 0
    comments: str = ''

class StudentCreate(StudentBase):
    group: str
    full_name: str
    term: float
    start_date: date
    profession: str
    category: int
    education_type_id: int
    login: str
    birth_date: date
    education_id: int
    payment: float
    protocol_number: str
    full_name_bel: str
    profession_bel: str

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

class StudentUpdate(StudentBase):
    id: int
    group: str | None = None
    full_name: str | None = None
    term: float | None = None
    start_date: date | None = None
    profession: str | None = None
    category: int | None = None
    education_type_id: int | None = None
    login: str | None = None
    birth_date: date | None = None
    education_id: int | None = None
    payment: float | None = None
    protocol_number: str | None = None
    full_name_bel: str | None = None
    profession_bel: str | None = None

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
    if student.category:
        db_student.category = student.category
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
