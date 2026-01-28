from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()


#GET POSTS
@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
        # cursor.execute('''SELECT * FROM posts''')
        # posts= cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

#CREATE POSTS
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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
@router.get("/posts/{id}", response_model=schemas.Post)
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
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/posts/{id}", response_model=schemas.Post)
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


