from sqlalchemy import Column, Integer, String, Float, ARRAY, Boolean
from models.students import Base


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
