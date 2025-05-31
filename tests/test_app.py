from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
        - A: Arrange - Arranjo
        - A: Act     - Executa a coisa (o SUT)
        - A: Assert  - Garanta que A é A
    """
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.json() == {"message": "Olá mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_aula_02_exericio():
    client = TestClient(app)
    response = client.get("/aula-02-exercicio")
    assert "<h1> Olá Mundo! </h1>" in response.text
