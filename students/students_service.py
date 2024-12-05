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


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    profession_id = Column(Integer)


Base.metadata.create_all(bind=engine)


class StudentCreate(BaseModel):
    name: str
    age: int
    education_type: int
    profession_id: int


@app.post("/students/")
def create_student(student: StudentCreate):
    db = SessionLocal()
    db_student = Student(name=student.name, age=student.age, profession_id=student.profession_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


AUTH_SERVICE_URL = "http://auth_service_url:8001/verify-token"

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    response = requests.get(AUTH_SERVICE_URL, headers={"Authorization": token})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.get('/protected')
def protected(user: dict = Depends(verify_token)):
    return {"msg": "You have access to this protected endpoint", "user": user}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8002)
