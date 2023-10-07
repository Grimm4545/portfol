from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemes.user import user_scheme, users_scheme
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix= "/usersdb",
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message" : "no encontrado"}})



user_list = []
@router.post("/", status_code= status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user_by_username(user.id)) == User:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "el usuario ya existe") 
    
    user_dict=dict(user)
    
    del user_dict["id"]
    id= db_client.local.users.insert_one(user_dict).inserted_id
    new_user=user_scheme( db_client.local.users.find_one({"_id": id}))
    
    return User(**new_user)

@router.get("/", response_model=list(User)) 
async def users():
    return users_scheme(db_client.local.users.find())

@router.get("/{id}", status_code= status.HTTP_201_CREATED)#antes del prefix este usaria /users/{id}, engorroso 
async def user(username: str):
   return search_user_by_username(username)



@router.get("/", status_code= status.HTTP_201_CREATED)
async def user(username: int):
    return search_user_by_username(username)

def search_user_by_username (username: str):
    
    try:
       user= db_client.local.user.find_one({"username": username})
       return User(**user_scheme(user))
    except:
        raise HTTPException(status_code= status.HTTP_302_FOUND, detail= "el usuario ya existe")



@router.put("/", status_code= status.HTTP_201_CREATED)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index]= index
            found= True
    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "no se encuentra")
        
    else:
        return user

#@router.get("/", response_model=list(user)) 
