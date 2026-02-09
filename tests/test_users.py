from fastapi.testclient import TestClient
from app import schemas
from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.createall(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


client =  TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Hello World From Ubuntu'
    assert res.status_code == 200
    
    
def test_create_user():
    res = client.post("/users/", json={"email":"hello@gmail.com", "password":"123456"})
    new_user = schemas.UserOp(**res.json())    
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
