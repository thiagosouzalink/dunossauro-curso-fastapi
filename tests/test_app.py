from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
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


def teste_create_user(client):
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


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"id": 1, "username": "alice", "email": "alice@example.com"}]
    }


def test_read_user_exercicio_03(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
    }


def test_invalid_param_read_user_exercicio_03(client):
    response = client.get("/users/404")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User Not Found"}


def test_update_user(client):
    response = client.put(
        "/users/1",
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


def test_invalid_param_update_user_exercicio_03(client):
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


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_invalid_param_delete_user_exercicio_03(client):
    response = client.delete("/users/404")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User Not Found"}


def test_exercicio_02_ola_mundo_html(client):
    response = client.get("/exercicio-02-ola-mundo-html")
    assert response.status_code == HTTPStatus.OK
    assert "<h1> Olá Mundo </h1>" in response.text
