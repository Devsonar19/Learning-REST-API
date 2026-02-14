from app import schemas
from jose import jwt
from app.config import settings
import pytest

# ROOT
def test_root(client):
    res = client.get("/")
    assert res.status_code == 200

# CREATE
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "123456"})
    new_user = schemas.UserOp(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

# LOGIN
def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(
        login_res.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    assert payload.get("user_id") == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@mail.com", "RightPassword", 403),
        ("rightemail@mail.com", "WrongPassword", 403),
        ("wrongemail@mail.com", "WrongPassword", 403),
        (None, "RightPassword", 422),
        ("rightemail@mail.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code
