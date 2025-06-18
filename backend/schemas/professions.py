from pydantic import BaseModel
from typing import List, Optional


class ProfessionBase(BaseModel):
    education_durations: Optional[List[str]] = None
    retraining_only: bool = False
    advance_duration: Optional[float] = None
    bondarenko: Optional[str] = None
    name_bel: Optional[str] = None
    has_google_link: bool = False
    has_grades: bool = False
    has_diary: bool = False


class ProfessionCreate(ProfessionBase):
    code: str
    name: str
    etks: str
    education_categories: List[str] = []


class ProfessionUpdate(ProfessionBase):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    etks: Optional[str] = None
    education_categories: Optional[List[str]] = []


class Profession(ProfessionBase):
    id: int
    code: str
    name: str
    etks: str
    education_categories: List[str]

    class Config:
        from_attributes = True


class ProfessionsHours(BaseModel):
    id: int
    duration: float
    theory_hours: int
    practice_hours: int

    class Config:
        from_attributes = True