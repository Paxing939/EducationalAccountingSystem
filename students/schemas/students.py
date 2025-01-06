from pydantic import BaseModel
from datetime import date


class StudentPayment(BaseModel):
    date: date
    amount: float


class StudentBase(BaseModel):
    referrer_organization: str | None = None
    theory_end_date: date | None = None
    practice_start_date: date | None = None
    practice_end_date: date | None = None
    end_date: date | None = None
    exam_date: date | None = None
    email: str | None = None
    previous_profession: str | None = None
    organization: str | None = None
    certificate_number: str | None = None
    grad_id: int | None = None
    practice_organization: str | None = None
    graduation_date: date | None = None
    grade_1: int | None = None
    grade_2: int | None = None
    payments: list[StudentPayment] = []
    theory_hours: int = 0
    practice_hours: int = 0
    status: int = 0
    comments: str = ''


class StudentCreate(StudentBase):
    group: str
    full_name: str
    term: float
    start_date: date
    profession: str
    degree: int
    education_type_id: int
    login: str
    birth_date: date
    education_id: int
    payment: float
    protocol_number: str
    full_name_bel: str
    profession_bel: str


class StudentUpdate(StudentBase):
    id: int
    group: str | None = None
    full_name: str | None = None
    term: float | None = None
    start_date: date | None = None
    profession: str | None = None
    degree: int | None = None
    education_type_id: int | None = None
    login: str | None = None
    birth_date: date | None = None
    education_id: int | None = None
    payment: float | None = None
    protocol_number: str | None = None
    full_name_bel: str | None = None
    profession_bel: str | None = None
