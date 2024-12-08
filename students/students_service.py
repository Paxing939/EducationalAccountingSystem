from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


@app.post("/students/")
def create_student(student: StudentCreate):
    print('new student is', student.name, student.age)
    db = SessionLocal()
    db_student = Student(name=student.name, age=student.age) #, profession_id=student.profession_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

