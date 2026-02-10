from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Hello World From Ubuntu'
    assert res.status_code == 200
    
    
def test_create_user(client):
    res = client.post("/users/", json={"email":"hello@gmail.com", "password":"123456"})
    new_user = schemas.UserOp(**res.json())    
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login", data={"username":"hello@gmail.com", "password":"123456"})
    assert res.status_code == 200