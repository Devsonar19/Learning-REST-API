from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field(default true)
    rating: Optional[int] = None


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

@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    return {"Using Array": my_posts}

@app.post("/posts")
def create_posts(newPost: Post):
    post_dict = newPost.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"Data": post_dict}