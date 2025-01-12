from sqlalchemy import Float, create_engine, Column, Integer, String, ARRAY, Boolean
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

Base.metadata.create_all(bind=engine)

def add_professions(professions: list[Profession]):
    db = SessionLocal()
    db.add_all(professions)
    db.commit()
    print(f"Added {len(professions)} entries to the database")
