from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Float, create_engine, Column, Integer, String, ARRAY, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if 'DATABASE_URL' not in os.environ:
    raise Exception('DATABASE_URL environment variable is not set')

DATABASE_URL = os.environ['DATABASE_URL']

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String, index=True)
    etks = Column(String, index=True)
    education_durations = Column(ARRAY(String), nullable=True)
    education_categories = Column(ARRAY(String))
    retraining_only = Column(Boolean, default=False)
    advance_duration = Column(Float, nullable=True)
    bondarenko = Column(String, nullable=True)
    name_bel = Column(String, nullable=True)
    has_google_link = Column(Boolean, default=False)
    has_grades = Column(Boolean, default=False)
    has_diary = Column(Boolean, default=False)

class ProfessionsHours(Base):
    __tablename__ = "professions_hours"
    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Float, index=True)
    theory_hours = Column(Integer, index=True)
    practice_hours = Column(Integer, index=True)

Base.metadata.create_all(bind=engine)


class ProfessionBase(BaseModel):
    education_durations: list[str] | None = None
    retraining_only: bool = False
    advance_duration: float | None = None
    bondarenko: str | None = None
    name_bel: str | None = None
    has_google_link: bool = False
    has_grades: bool = False
    has_diary: bool = False

class ProfessionCreate(ProfessionBase):
    code: str
    name: str
    etks: str
    education_categories: list[str] = []

@app.post("/professions/create")
def create_profession(profession: ProfessionCreate):
    db = SessionLocal()
    db_profession = Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession

class ProfessionUpdate(ProfessionBase):
    id: int
    code: str | None = None
    name: str | None = None
    etks: str | None = None
    education_categories: list[str] | None = []

@app.post("/professions/edit")
def edit_profession(profession: ProfessionUpdate):
    db = SessionLocal()
    db_profession = db.query(Profession).filter(Profession.id == profession.id).first()
    if db_profession is None:
        raise HTTPException(status_code=400, detail="Profession not found")
    if profession.name:
        db_profession.name = profession.name
    if profession.code:
        db_profession.code = profession.code
    if profession.etks:
        db_profession.etks = profession.etks
    if profession.education_categories:
        db_profession.education_categories = profession.education_categories
    db_profession.education_durations = profession.education_durations
    db_profession.retraining_only = profession.retraining_only
    db_profession.advance_duration = profession.advance_duration
    db_profession.bondarenko = profession.bondarenko
    db_profession.name_bel = profession.name_bel
    db_profession.has_google_link = profession.has_google_link
    db_profession.has_grades = profession.has_grades
    db_profession.has_diary = profession.has_diary
    db.commit()
    db.refresh(db_profession)
    return db_profession

@app.get("/professions")
def get_professions():
    db = SessionLocal()
    db_professions = db.query(Profession).all()
    return db_professions

@app.get("/professions_hours")
def get_professions_hours():
    db = SessionLocal()
    db_professions_hours = db.query(ProfessionsHours).all()
    return db_professions_hours

@app.get("/professions/{id}")
def get_profession(id: int):
    db = SessionLocal()
    db_profession = db.query(Profession).filter(Profession.id == id).first()
    if db_profession is None:
        raise HTTPException(status_code=400, detail="Profession not found")
    return db_profession

@app.get("/professions/by/name/{name}")
def get_profession_by_name(name: str):
    db = SessionLocal()
    db_profession = db.query(Profession).filter(Profession.name == name).first()
    if db_profession is None:
        raise HTTPException(status_code=400, detail="Profession not found")
    return db_profession
