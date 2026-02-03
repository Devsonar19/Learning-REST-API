from .. import models, schemas, utils, oauth
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#GET POSTS
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth.get_current_user),
    limit : int = 10,
    skip : int = 0,
    search : Optional[str] = ""
    ):
    posts = (
        db.query(models.Post)
        .options(joinedload(models.Post.owner))
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    print(results)

    return results


#CREATE POSTS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(newPost: schemas.PostCreate, db : Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
        # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
        #                 (newPost.title, newPost.content, newPost.published)) #not using f string because it's prone to sql injection
        # posts = cursor.fetchone()
        # conn.commit()
    newPost= models.Post(owner_id = get_current_user.id, **newPost.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost
    
#GET POSTS BY ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user=Depends(oauth.get_current_user)
):
    post = (
        db.query(models.Post)
        .options(joinedload(models.Post.owner))
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found"
        )

    return post



#DELETE POSTS BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
   
        # cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''', (str(id)))
        # delete_post = cursor.fetchone()
        # conn.commit()

    delete_post = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform action')

    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#UPDATE POSTS BY ID
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post:schemas.PostCreate, db : Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):

        # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published,str(id)))

        # updated_posts= cursor.fetchone()
        # conn.commit()

    updated_posts = db.query(models.Post).filter(models.Post.id == id)
    up_posts = updated_posts.first()

    if up_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")
    

    if up_posts.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform action')

    updated_posts.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_posts.first()


