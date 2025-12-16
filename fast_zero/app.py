from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()

html_file = Path(__file__).parent / "templates/ola_mundo.html"


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.get(
    "/exercicio-02-ola-mundo-html",
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def read_exercicio_02_ola_mundo_html():
    return html_file.read_text(encoding="utf-8")
