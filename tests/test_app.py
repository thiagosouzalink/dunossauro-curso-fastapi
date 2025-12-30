from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client: TestClient):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act     - Executa a coisa
    - A: Assert  - Garanta que A é A
    """
    # act
    response = client.get("/")

    # assert
    assert response.json() == {"message": "Olá Mundo!"}
    assert response.status_code == HTTPStatus.OK


def teste_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
    }


def test_create_user_with_username_conflict_exercicio_05(
    client: TestClient, user: User
):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_with_email_conflict_exercicio_05(
    client: TestClient, user: User
):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": user.email,
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client: TestClient, user: User, token: str):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user_exercicio_03(client: TestClient, user: User):
    response = client.get(f"/users/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def test_invalid_param_read_user_exercicio_03(client: TestClient, user: User):
    response = client.get("/users/404")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User Not Found"}


def test_update_user(client: TestClient, user: User, token: str):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_integrity_error(client: TestClient, user: User, token: str):
    client.post(
        "/users/",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username or Email already exists"}


def test_invalid_param_update_user_exercicio_03(
    client: TestClient, user: User
):
    response = client.put(
        "/users/404",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User Not Found"}


def test_delete_user(client: TestClient, user: User, token: str):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_invalid_param_delete_user_exercicio_03(
    client: TestClient, user: User
):
    response = client.delete("/users/404")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User Not Found"}


def test_exercicio_02_ola_mundo_html(client: TestClient):
    response = client.get("/exercicio-02-ola-mundo-html")
    assert response.status_code == HTTPStatus.OK
    assert "<h1> Olá Mundo </h1>" in response.text


def test_get_token(client: TestClient, user: User):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
