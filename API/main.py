from fastapi import FastAPI
from routers import products, users, basicauthusers, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles



app=FastAPI()

#router
app.include_router(products.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router)
app.include_router(basicauthusers.router)
app.include_router(users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/url")
async def url():
    return {"bienvenidos a franco.com"}

    
#inicio del server: uvicorn main:app --reload#
#apagado del server: ctrl+c#
#from fastapi import FastAPI
#app = FastAPI()
#@app.get("/url")
#async def root():
#    return{"bienvenidos a franco.com"}
