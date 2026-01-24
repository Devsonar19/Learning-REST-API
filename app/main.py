from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


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

#GET POSTS
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
        # cursor.execute('''SELECT * FROM posts''')
        # posts= cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

#CREATE POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(newPost: schemas.PostCreate, db : Session = Depends(get_db)):
        # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
        #                 (newPost.title, newPost.content, newPost.published)) #not using f string because it's prone to sql injection
        # posts = cursor.fetchone()
        # conn.commit()
    newPost= models.Post(**newPost.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost
    
#GET POSTS BY ID
@app.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id: int, db : Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"Post with {id} was not found"}
    return post


#DELETE POSTS BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
   
        # cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''', (str(id)))
        # delete_post = cursor.fetchone()
        # conn.commit()

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")

    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#UPDATE POSTS BY ID
@app.put("/posts/{id}", response_model=schemas.Post)
def update_posts(id: int, post:schemas.PostCreate, db : Session = Depends(get_db)):

        # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published,str(id)))

        # updated_posts= cursor.fetchone()
        # conn.commit()

    updated_posts = db.query(models.Post).filter(models.Post.id == id)
    up_posts = updated_posts.first()

    if up_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")
    
    updated_posts.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_posts.first()
