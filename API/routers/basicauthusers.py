#mecanismos de seguridad pasicos para autenticar un usuario
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router= APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl= "login")


class User(BaseModel):
    username: str
    Nombre: str
    Apellido: str
    Edad: int
    disebled: bool

class User_DB(User):
    password: str
    
users_db ={ 
           "francop": {
                    "username":"francop" ,
                    "Nombre": "Franco",
                    "Apellido": "Colombo" ,
                    "Edad": "27" ,
                    "disebled": False,
                    "password": "12345"
                    },
            "francop1": {
                    "username":"francop1" ,
                    "Nombre": "Franco1",
                    "Apellido": "Colombo1" ,
                    "Edad": "24" ,
                    "disebled": True,
                    "password": "54321"
                    }
           }

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return User_DB(**users_db[username])

#ahora hacemos la autenticacion BASICA
async def current_user(token: str= Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail= "credenciales de autenticacion invalidas",
                            headers= {"www-Authenticate": "Bearer"})
    if user.disebled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "usuario inactivo")
    return user

@router.post("/login1")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    user_db= users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "usuario, no es correcto")
    user = search_user_db(form.username)
    if not form.password ==  user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "password, no es correcto")
    return {"user": user.username, "password":"correct!"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
