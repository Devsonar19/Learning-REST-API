from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")   #Decorator, without it, its simple python
def root():
    return {"message": "Hello World From Ubuntu"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createpost")
def create_posts(payLoad : dict = Body(...)):
    print(payLoad)
    return {"Info about Post": f"Title: {payLoad['title']} Content: {payLoad['content']}"}