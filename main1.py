#inicio del server: uvicorn main:app --reload#
#apagado del server: ctrl+c#
#fastapi sibe para trabajar los datos sencillos
#HTTPException nos da la listas de codigos error clasicos que audara a otros programadores
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel #sirve para definir una entidad o usuairios, con mecanismos integrados#

app = FastAPI()
@app.get("/")
#@app.get() pide datos#
async def root():
    return{"message":"Hello World"}

class User(BaseModel):
    id: int
    Nombre: str
    Apellido: str
    url: str
    
user_list = [User (id= 1, Nombre = "Franco", Apellido= "Colombo", url= "https//cofran.com"),
             User (id= 2, Nombre = "Nora", Apellido= "Knez", url= "https//knezno.com"),
             User (id= 3, Nombre = "Martina", Apellido= "Colombo", url= "https//martuco.com")   
]#contiene todos los usuarios
@app.get("/users", status_code= 201)
async def users():
    return [{"Nombre" : "Franco", "Apellido": "Colombo", "url": "https//cofran.com"},
           {"Nombre": "Martina", "Apellido": "Colombo", "url": "https//comartu.com"}]
#es brusco ya que tendrias que llenar uno por uno los pedidos en back end
#para ser mas practico definimos usuario como entidad y le damos parametros mas flaxibles
@app.get("/user/", status_code= 201)
async def user():
    return user_list#no necesito haces mas engorroso el codigo gracias a esto

#como usar path para administrar informacios especificamente
@app.get("/user/{id}", status_code= 201)
async def user(id: int):
   return search_user(id)#busqueda usuario esta definido como una funcion debajo para buscar id especifica
#ahora como seria query que es la alternativa a path
@app.get("/user/", status_code= 201)
async def user(id: int):
    return search_user(id)
#funciona igual que el path pero en el tipeo de la url entra en funcion  con /?id=
@app.get("/usersjson/", status_code= 201)
async def usersjson():
    return [User (id= 1, Nombre = "Franco", Apellido= "Colombo", url= "https//cofran.com"),
             User (id= 2, Nombre = "Nora", Apellido= "Knez", url= "https//knezno.com"),
             User (id= 3, Nombre = "Martina", Apellido= "Colombo", url= "https//martuco.com")   
]

def search_user (id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code= 404, detail= "no se encuentra usuario")
        #return {"eror": "no se encuentra usuario"}


#sumar usuarios
#@app.post("/user/")#@app.post() crea datos
#async def user(user: User):
#    if type(search_user(user.id)) == User:
#        return {"error! El usuario ya existe"}
#    else:
#        user_list.append(user)
#        return user
    

#ahora lo mismo pero usando los codigos de http para ayudas y agilizar
@app.post("/user/", status_code= 201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 404, detail= "el usuario ya existe") 
    user_list.append(user)
    return user

@app.put("/user/", status_code= 201)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index]= index
            found= True
    if not found:
        raise HTTPException(status_code= 404, detail= "no se encuentra")
        #return {"no se encuentra el usuario"} se puede usar pero no es tan intuirtivo
    else:
        return user
#solo los usuarios despues del id 4, va a poder modificarse
#del id 1 al 3 estos estan "escritos en peidra" en el progama por practicas anteriores
@app.delete("/user/{id}", status_code= 201)#con esto podemos eliminar un usuario especifico
async def user(id: int):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True
    if not found:
        raise HTTPException(status_code= 404, detail= "no se elimino el usuario")
        #return {"no se elimino el usuario"}