from typing import List

import pytest
from app import models, schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title":"1st title",
            "content":"1st content",
            "owner_id":test_user['id']
        },
        {
            "title":"2nd title",
            "content":"2nd content",
            "owner_id":test_user['id']
        },
        {
            "title":"3rd title",
            "content":"3rd content",
            "owner_id":test_user['id']
        }
    ]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    list_posts = list(post_map)

    session.add_all(list_posts)
    session.commit()
    res = session.query(models.Post).all()
    return res

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_one_post_not_exit(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/6969")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    