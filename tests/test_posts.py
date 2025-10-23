import pytest
from app.schemas import posts


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# def test_unauthorized_user_get_all_posts(client, test_posts):
#     res = client.get("/posts")
#     assert res.status_code == 401


def test_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    this_post = posts.PostOut(**res.json())
    assert this_post.id == test_posts[0].id
    assert this_post.name == test_posts[0].name
    assert res.status_code == 200


def test_get_post_does_not_exist(client, test_posts):
    res = client.get("/posts/999")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "name, content, is_published",
    [
        ("Pizza", "New Pizza Spot", False),
        ("Pizza Test", "New Pizza Spot", False),
        ("Pizza User", "New Pizza Spot", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, name, content, is_published
):
    res = authorized_client.post(
        "/posts", json={"name": name, "content": content, "is_published": is_published}
    )
    created_post = posts.PostOut(**res.json())

    assert res.status_code == 201
    assert created_post.name == name
    assert created_post.content == content
    assert created_post.is_published == is_published
    assert created_post.user_id == test_user["id"]


def test_default_is_published_is_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts", json={"name": "new name", "content": "test"})

    created_post = posts.PostOut(**res.json())
    assert res.status_code == 201
    assert res.json()["is_published"] is True
    assert created_post.user_id == test_user["id"]


def test_create_post_unauthorized(client, test_user, test_posts):
    res = client.post(
        "/posts",
        json={
            "name": "test name",
            "content": "test content",
            "is_published": "test published",
        },
    )
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/999")
    assert res.status_code == 404


def test_delete_post_unauthorized(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_updated_post(authorized_client, test_user, test_posts):
    data = {"name": "Updated Name", "content": "Updated Content", "is_published": False}

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = posts.PostOut(**res.json())
    assert updated_post.name == data["name"]
    assert updated_post.content == data["content"]
    assert updated_post.is_published == data["is_published"]
    assert res.status_code == 202


def test_updated_post_unauthorized(client, test_user, test_posts):
    data = {"name": "Updated Name", "content": "Updated Content", "is_published": False}

    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {"name": "Updated Name", "content": "Updated Content", "is_published": False}

    res = authorized_client.put("/posts/999", json=data)
    assert res.status_code == 404
