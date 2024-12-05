# auth_service.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = "your_secret_key"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

class User(BaseModel):
    username: str
    password: str

fake_db = {
    "test": {
        "username": "test",
        "password": "test"
    }
}

@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username not in fake_db or fake_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Bad username or password")
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}

@app.get('/verify-token')
def verify_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
