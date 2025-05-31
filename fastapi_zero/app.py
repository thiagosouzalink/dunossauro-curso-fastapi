from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá mundo!"}


@app.get(
    "/aula-02-exercicio",
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def aula_02_exercicio():
    return """
    <html>
      <head>
        <title>ola-mundo</title>
      </head>
      <body>
        <h1> Olá Mundo! </h1>
      </body>
    </html>
    """
