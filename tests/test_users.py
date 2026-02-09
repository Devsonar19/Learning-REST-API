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
import pytest

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def session():
    # we can run after test finishes
    Base.metadata.dropall(bind=engine)
    # we can run code before we run our test
    Base.metadata.createall(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    



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
