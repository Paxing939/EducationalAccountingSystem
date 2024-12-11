from fastapi import FastAPI, HTTPException, Depends, Response
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(creds: UserLoginSchema, response: Response):

    if(creds.username == "Admin1" and creds.password == "df23f"):
        token = security.create_access_token(uid="1")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль.")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected(Authorize: AuthX = Depends()):
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
