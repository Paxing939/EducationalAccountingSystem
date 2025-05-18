from sqlalchemy import Float, create_engine, Column, Integer, String, ARRAY, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://user:password@localhost:5443/students_db'

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

def add_professions(professions: list[Profession]):
    db = SessionLocal()
    db.add_all(professions)
    db.commit()
    print(f"Added {len(professions)} entries to the database")

def get_profession(profession: Profession) -> Profession:
    db = SessionLocal()
    result = db.query(Profession).filter(func.lower(Profession.name) == func.lower(profession.name.replace('ё', 'е'))).first()
    db.close()
    return result

def add_hours(hours: list[ProfessionsHours]):
    db = SessionLocal()
    db.add_all(hours)
    db.commit()
    print(f"Added {len(hours)} entries to the database")

