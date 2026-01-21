from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field(default true)
    
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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        




@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts= cursor.fetchall()
    print(posts)
    return {"From DB": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(newPost: Post):
    cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
                    (newPost.title, newPost.content, newPost.published))
    posts = cursor.fetchone()
    conn.commit()
    return {"Data": posts}
    

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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has required ID
    #my_posts.pop(index) 
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not Exists")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
