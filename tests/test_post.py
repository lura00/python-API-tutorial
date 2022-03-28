import pytest
from app import schema
from app.models import Post


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schema.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(list(posts_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostOut(**res.json())
    # assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("my new post 1", "My new content 1", True),
    ("my new post 2", "My new content 2", False),
    ("my new post 3", "My new content 3", True),
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "some title", "content": "some content"})

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "some title"
    assert created_post.content == "some content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.post(
        "/posts/", json={"title": "some title", "content": "some content"})
    assert res.status_code == 401


def test_unathorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_udpate_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unathorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404
