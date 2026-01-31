from fastapi import FastAPI 
from . import models
from .routers import post, user, auth
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind = engine)


#ROOT GET
@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)