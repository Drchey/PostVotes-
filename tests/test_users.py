from app.schemas import users, token
import pytest
from jose import jwt  # type: ignore
from app.config import settings


@pytest.fixture
def test_create_user(client):
    res = client.post(
        "/users", json={"email": "johndoe@gmail.com", "password": "password123"}
    )
    new_user = users.UserOut(**res.json())
    assert new_user.email == "johndoe@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = token.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "secretpassword", 401),
        ("johndoe@gmail.com", "wrongsecretpassword", 401),
    ],
)
def test_incorrect_login_user(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
