from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM= "HS256"
ACCESS_TOKEN_DURATION= 1
SECRET= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

router= APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl= "login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    Nombre: str
    Apellido: str
    Edad: int
    disebled: bool

class User_DB(User):
    password: str
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return User_DB(**users_db[username])


users_db ={ 
           "francop": {
                    "username":"francop" ,
                    "Nombre": "Franco",
                    "Apellido": "Colombo" ,
                    "Edad": "27" ,
                    "disebled": False,
                    "password": "$2a$12$l3jaIJQDTJvFOAiwMB3AUuEwXrmvhdvu7vzqUl0JZSIy/aMcnrEFC"
                    },
            "francop1": {
                    "username":"francop1" ,
                    "Nombre": "Franco1",
                    "Apellido": "Colombo1" ,
                    "Edad": "24" ,
                    "disebled": True,
                    "password": "$2a$12$6H1tk110KcbjVsXiIBueeezVho2SclMD/Vf9eNmvO7Vnl682vcSZa"
                    }
           }

async def auth_user(token: str= Depends(oauth2)):
    exeption= HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED, 
                detail= "credenciales de autenticacion invalidas",
                headers= {"www-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms= ALGORITHM).get("sub")
        if username is None:
            raise exeption
    
    except JWTError:
         raise exeption
    
    return search_user(username)
    

async def current_user(user: User= Depends(auth_user)):
    exeption= HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED, 
                detail= "credenciales de autenticacion invalidas",
                headers= {"www-Authenticate": "Bearer"})
    if user.disebled:
        raise exeption
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    user_db= users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "usuario, no es correcto")
    user = search_user_db(form.username)
    
    crypt.verify(form.password, user.password)
    if not form.password ==  user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "password, no es correcto")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}

@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user