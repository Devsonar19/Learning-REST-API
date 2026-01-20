from fastapi import FastAPI, Response, status, HTTPException
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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    return {"Using Array": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(newPost: Post):
    post_dict = newPost.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"Data": post_dict}
    

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post =  find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"Post with {id} was not found"}
    return{"post_detail": post}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}
