from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import pytest
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient
from app.oauth import create_access_token


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {"email":"hello@gmail.com", "password":"123456"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user = ['password'] = user_data['password']
    return new_user



@pytest.fixture
def session():
    # we can run after test finishes
    #running fixtures
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
    
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

