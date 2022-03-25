import pytest
from jose import jwt
from app import schema
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello1234@gmail.com", "password": "testpass"})

    # User pydantic models to do some validation
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello1234@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'testpass', 403),
    ('lura@gmail.com', 'wrongpass', 403),
    ('wrongemail@gmail.com', 'Wrongpass', 403),
    (None, 'testpass', 422),
    ('lura@gmail.com', None, 422)
])
def test_incprrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
