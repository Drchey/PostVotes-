import pytest
from app.database import Base, engine, SessionLocal
from fastapi.testclient import TestClient
from app.main import app
from app.router import oauth2
from app import models


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # run our code before we run our test
    yield TestClient(app)
    # run our code after our test finished


@pytest.fixture
def test_user(client):
    user_data = {"email": "johndoe@gmail.com", "password": "secretpassword"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token(
        {"user_id": test_user["id"], "sub": test_user["email"]}
    )


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "name": "Test Title[1]",
            "content": "1st Content",
            "user_id": test_user["id"],
        },
        {
            "name": "Test Title[2]",
            "content": "2nd Content",
            "user_id": test_user["id"],
        },
        {
            "name": "Test Title[3]",
            "content": "3rd Content",
            "user_id": test_user["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
