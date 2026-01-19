from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field(default true)
    rating: Optional[int] = None


@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createpost")
def create_posts(newPost: Post):
    print(newPost.rating)
    print(newPost.dict)
    return {"Data": newPost}