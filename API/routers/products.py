from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router=APIRouter(prefix="/products" ) 
#APIRouter(prefix="/products") reemplaza tener que poner la "carpeta original "todo el tiempo 
class fruta(BaseModel):
    id: int
    nombre: str
    
product_list = [fruta (id= 1, nombre="producto 1" ), 
               fruta (id= 2, nombre= "producto 2"),
               fruta (id= 3, nombre= "producto 3"),
               fruta (id= 4, nombre= "producto 4"),
               fruta (id= 5, nombre= "producto 5"),]

def search_product (id: int):
    products = filter(lambda product: product.id == id, product_list)
    try:
        return list(products)[0]
    except:
        raise HTTPException(status_code= 404, detail= "no se encuentra producto")

@router.get("/", status_code= 201) 
async def user():
    return product_list
@router.get("/{id}", status_code= 201)
async def user(id: int):
   return search_product(id)