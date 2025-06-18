from fastapi import HTTPException
from schemas.professions import *
from models.professions import *
from students_service import app, SessionLocal


@app.post("/professions/create")
def create_profession(profession: ProfessionCreate):
    db = SessionLocal()
    db_profession = Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession

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
