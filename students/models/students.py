from sqlalchemy import Column, Integer, String, Date, Float, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EducationType(Base):
    __tablename__ = "education_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))


class Education(Base):
    __tablename__ = "educations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    referrer_organization = Column(String(256), nullable=True)
    group = Column(String(10))
    full_name = Column(String(128))
    term = Column(Float)
    start_date = Column(Date)
    theory_end_date = Column(Date, nullable=True)
    practice_start_date = Column(Date, nullable=True)
    practice_end_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    exam_date = Column(Date, nullable=True)
    profession = Column(String(256))
    degree = Column(Integer)
    education_type_id = Column(Integer, ForeignKey(EducationType.id))
    login = Column(String(128))
    email = Column(String(128), nullable=True)
    birth_date = Column(Date)
    education_id = Column(Integer, ForeignKey(Education.id))
    previous_profession = Column(String(256), nullable=True)
    payment = Column(Float)
    organization = Column(String(256), nullable=True)
    protocol_number = Column(String(20))
    certificate_number = Column(String(20), nullable=True)
    grad_id = Column(Integer, nullable=True)
    theory_hours = Column(Integer, default=0)
    practice_hours = Column(Integer, default=0)
    practice_organization = Column(String(256), nullable=True)
    status = Column(Integer, default=0)
    payments = Column(ARRAY(JSONB), default=[])
    comments = Column(String(256), default='')
    graduation_date = Column(Date, nullable=True)
    grade_1 = Column(Integer, nullable=True)
    grade_2 = Column(Integer, nullable=True)
    full_name_bel = Column(String(128))
    profession_bel = Column(String(256))
