from fastapi.testclient import TestClient
from app.main import app

client =  TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Hello World From Ubuntu'
    assert res.status_code == 200
    
    
def test_create_user():
    res = client.post("/users/", json={"email":"hello@gmail.com", "password":"123456"})
    print(res.json())
    assert res.json().get("email") == "hello@gmail.com"
    assert res.status_code == 201
