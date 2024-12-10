from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Float, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgres_db:5432/students_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    train_1 = Column(Float, nullable=True)
    train_2 = Column(Float, nullable=True)
    train_3 = Column(Float, nullable=True)
    train_4 = Column(Float, nullable=True)
    retrain_1 = Column(Float, nullable=True)
    retrain_2 = Column(Float, nullable=True)
    retrain_3 = Column(Float, nullable=True)
    retrain_4 = Column(Float, nullable=True)
    advancement = Column(Float, nullable=True)

Base.metadata.create_all(bind=engine)


class ProfessionBase(BaseModel):
    train_1: float | None = None
    train_2: float | None = None
    train_3: float | None = None
    train_4: float | None = None
    retrain_1: float | None = None
    retrain_2: float | None = None
    retrain_3: float | None = None
    retrain_4: float | None = None
    advancement: float | None = None

class ProfessionCreate(ProfessionBase):
    name: str

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
    name: str | None = None

@app.post("/professions/edit")
def edit_profession(profession: ProfessionUpdate):
    db = SessionLocal()
    db_profession = db.query(Profession).filter(Profession.id == profession.id).first()
    if db_profession is None:
        raise HTTPException(status_code=400, detail="Profession not found")
    if profession.name:
        db_profession.name = profession.name
    db_profession.train_1 = profession.train_1
    db_profession.train_2 = profession.train_2
    db_profession.train_3 = profession.train_3
    db_profession.train_4 = profession.train_4
    db_profession.retrain_1 = profession.retrain_1
    db_profession.retrain_2 = profession.retrain_2
    db_profession.retrain_3 = profession.retrain_3
    db_profession.retrain_4 = profession.retrain_4
    db_profession.advancement = profession.advancement
    db.commit()
    db.refresh(db_profession)
    return db_profession
