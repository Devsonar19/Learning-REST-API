from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

from .routers import post, user


app = FastAPI()

models.Base.metadata.create_all(bind = engine)

    
#CONNECTING DB
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapiDB', user = 'postgres', password='318204', cursor_factory=RealDictCursor)
        
        cursor =  conn.cursor()
        print('Database Connection Succesfull.!!')
        break
    except Exception as error:
        print("Connection Failed")
        print("Error: ", error)
        time.sleep(2) #will keep trying to connect ever t sec

#EXAMPLE POST
my_posts = [
    {
        "title":"example post 1",
        "content":"Exampleeee",
        "id":1 
    },
    {
        "title":"example post 2",
        "content":"ExampleeeeYYYY",
        "id":2
    }
]

#FIND FUNCTIONS
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        


#ROOT GET
@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}



app.include_router(post.router)
app.include_router(user.router)