from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Float, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgres_db:5432/educational_db"

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


class ProfessionCreate(BaseModel):
    name: str
    train_1: float | None = None
    train_2: float | None = None
    train_3: float | None = None
    train_4: float | None = None
    retrain_1: float | None = None
    retrain_2: float | None = None
    retrain_3: float | None = None
    retrain_4: float | None = None
    advancement: float | None = None


@app.post("/professions/")
def create_profession(profession: ProfessionCreate):
    db = SessionLocal()
    db_profession = Profession(name=profession.name,
                               train_1=profession.train_1, train_2=profession.train_2, train_3=profession.train_3, train_4=profession.train_4,
                               retrain_1=profession.retrain_1, retrain_2=profession.retrain_2, retrain_3=profession.retrain_3, retrain_4=profession.retrain_4,
                               advancement=profession.advancement)
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession
