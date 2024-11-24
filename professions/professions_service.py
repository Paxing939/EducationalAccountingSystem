from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/educational_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


Base.metadata.create_all(bind=engine)


class ProfessionCreate(BaseModel):
    name: str


@app.post("/professions/")
def create_profession(profession: ProfessionCreate):
    db = SessionLocal()
    db_profession = Profession(name=profession.name)
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession
