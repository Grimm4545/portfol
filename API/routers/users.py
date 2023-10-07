#inicio del server: uvicorn main:app --reload#
#apagado del server: ctrl+c#
from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel

router = APIRouter(prefix= "/users")
#APIRouter(prefix="/products") reemplaza tener que poner la "carpeta original " todo el tiempo

class User(BaseModel):
    id: int
    Nombre: str
    Apellido: str
    url: str
user_list = [User (id= 1, Nombre = "Franco", Apellido= "Colombo", url= "https//cofran.com"),
             User (id= 2, Nombre = "Nora", Apellido= "Knez", url= "https//knezno.com"),
             User (id= 3, Nombre = "Martina", Apellido= "Colombo", url= "https//martuco.com")]
@router.get("/", status_code= 201) 
async def user():
    return user_list
@router.get("/{id}", status_code= 201)#antes del prefix este usaria /users/{id}, engorroso 
async def user(id: int):
   return search_user(id)
@router.get("/", status_code= 201)
async def user(id: int):
    return search_user(id)

def search_user (id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code= 404, detail= "no se encuentra usuario")

@router.post("/", status_code= 201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 404, detail= "el usuario ya existe") 
    user_list.append(user)
    return user


@router.put("/", status_code= 201)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index]= index
            found= True
    if not found:
        raise HTTPException(status_code= 404, detail= "no se encuentra")
        
    else:
        return user

@router.delete("/{id}", status_code= 201)
async def user(id: int):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True
    if not found:
        raise HTTPException(status_code= 404, detail= "no se elimino el usuario")