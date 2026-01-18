from fastapi import FastAPI

app = FastAPI()


@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}