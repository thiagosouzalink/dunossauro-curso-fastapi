from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Curso de FastAPI")

database = []
app = FastAPI()

html_file = Path(__file__).parent / "templates/ola_mundo.html"


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


@app.put(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User Not Found"
        )
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User Not Found"
        )
    return database.pop(user_id - 1)


@app.get(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User Not Found"
        )
    return database[user_id - 1]


@app.get(
    "/exercicio-02-ola-mundo-html",
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def read_exercicio_02_ola_mundo_html():
    return html_file.read_text(encoding="utf-8")
