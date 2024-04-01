from ..app.schemas.user import UserCreate
from .conftest import client,session
import pytest
from ..app.routes.user import userRoute

user_credentials = {"email": "ucero@gmail.com", "password": "password"}
@pytest.fixture
def test_user(client):
    response = client.post(userRoute.prefix,json=user_credentials,)
    print(response.json())
    assert response.status_code == 201
    newUser = response.json()

    return newUser

def test_connection_db(session):
    assert session is not None

def test_create_user(client):
    response = client.post(userRoute.prefix,json=user_credentials,)
    print(response.json())
    assert response.status_code == 201
    assert user_credentials["email"] == response.json()["email"]
    #2nd time should fail
    response = client.post(userRoute.prefix,json=user_credentials,)
    assert response.status_code == 400 and response.json() == {"detail": "Email already registered"}


def test_create_user_invalid_email(client):
    response = client.post(userRoute.prefix,
                           json={"email": "3453", "password": "password"}, )
    assert response.status_code == 422

def test_get_users(client, test_user):
    response = client.get(userRoute.prefix)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

