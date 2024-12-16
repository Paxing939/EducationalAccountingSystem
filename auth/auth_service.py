from fastapi import FastAPI, HTTPException, Depends, Response
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)
token = ""
class UserLoginSchema(BaseModel):
    username: str
    password: str
def read_users_from_file(file_path: str):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password = line.strip().split()
            users[username] = password
    return users
@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    users = read_users_from_file('testLoginsAndPasswords.txt')
    if creds.username in users and users[creds.username] == creds.password:
        token = security.create_access_token(uid="1")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль.")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return True
