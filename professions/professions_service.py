from fastapi import FastAPI, HTTPException
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


class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String, index=True)
    etks = Column(String, index=True)
    education_durations = Column(ARRAY(String), nullable=True)
    education_categories = Column(ARRAY(String))
    retraining_only = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)


class ProfessionBase(BaseModel):
    education_durations: list[str] | None = None
    retraining_only: bool = False

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
    db.commit()
    db.refresh(db_profession)
    return db_profession
