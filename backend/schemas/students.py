from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class PaymentBase(BaseModel):
    amount: float
    date: date
    type: str


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    referrer_organization: Optional[str] = None
    group: str
    full_name: str
    term: float
    start_date: date
    theory_end_date: Optional[date] = None
    practice_start_date: Optional[date] = None
    practice_end_date: Optional[date] = None
    end_date: Optional[date] = None
    exam_date: Optional[str] = None
    profession: str
    degree: int
    education_type_id: int
    login: str
    email: Optional[str] = None
    birth_date: date
    education_id: int
    previous_profession: Optional[str] = None
    payment: float
    organization: Optional[str] = None
    protocol_number: str
    certificate_number: Optional[str] = None
    grad_id: Optional[int] = None
    theory_hours: int = 0
    practice_hours: int = 0
    practice_organization: Optional[str] = None
    status: int
    payments: List[PaymentCreate] = []
    comments: str = ''
    graduation_date: Optional[date] = None
    grade_1: Optional[int] = None
    grade_2: Optional[int] = None
    full_name_bel: str
    profession_bel: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    id: int
    referrer_organization: Optional[str] = None
    group: Optional[str] = None
    full_name: Optional[str] = None
    term: Optional[float] = None
    start_date: Optional[date] = None
    theory_end_date: Optional[date] = None
    practice_start_date: Optional[date] = None
    practice_end_date: Optional[date] = None
    end_date: Optional[date] = None
    exam_date: Optional[str] = None
    profession: Optional[str] = None
    degree: Optional[int] = None
    education_type_id: Optional[int] = None
    login: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None
    education_id: Optional[int] = None
    previous_profession: Optional[str] = None
    payment: Optional[float] = None
    organization: Optional[str] = None
    protocol_number: Optional[str] = None
    certificate_number: Optional[str] = None
    grad_id: Optional[int] = None
    theory_hours: Optional[int] = None
    practice_hours: Optional[int] = None
    practice_organization: Optional[str] = None
    status: Optional[int] = None
    payments: Optional[List[PaymentCreate]] = None
    comments: Optional[str] = None
    graduation_date: Optional[date] = None
    grade_1: Optional[int] = None
    grade_2: Optional[int] = None
    full_name_bel: Optional[str] = None
    profession_bel: Optional[str] = None


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True


class EducationType(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Education(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StudentStatus(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
