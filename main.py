from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
from exceptions import UserExistsException, PerevalExistsException


description = """
На сайте https://pereval.online/ ФСТР ведёт базу горных перевалов, которая пополняется туристами.
Проект ФСТР "Перевал Online" создан специально для горных путешественников.

## Отправка информации на сервер о перевале
для мобильного приложения ФСТР. 🚀
"""


app = FastAPI(
    title="REST API FSTR",
    description=description,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {
    "method GET": "/pereval/{id} - получить данные о перевале по id",
    "method POST": "/submitData/ - отправить данные о перевале (принимает JSON)",
}


# получить одну запись (перевал) по её id.
@app.get("/pereval/{id}/", response_model=schemas.AddedBase)
def read_pereval(id: int, db: Session = Depends(get_db)):
    pereval = crud.get_pereval(db, id=id)
    if not pereval:
        raise PerevalExistsException(id=id)
    return crud.get_pereval(db, id=id)


# отправить данные о перевале
@app.post("/submitData/", response_model=schemas.AddedBase)
def add_pereval(raw_data: schemas.AddedRaw, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=raw_data.user.email)
    if db_user:
        raise UserExistsException(email=db_user.email)

    user = crud.create_user(db, user=raw_data.user)
    coords = crud.create_coords(db, coords=raw_data.coords)
    level = crud.create_level(db, level=raw_data.level)
    foto = crud.add_foto(db, foto=raw_data.images)
    pereval = crud.create_pereval(db, raw_data, user, coords, level)
    images = crud.add_relation(db, pereval.id, foto)
    return JSONResponse(status_code=200, content={"status": 200, "message": "Отправлено успешно", "id": pereval.id})


@app.exception_handler(UserExistsException)
async def user_exists_handler(request: Request, exc: UserExistsException):
    return JSONResponse(
        status_code=400,
        content={"status" : 400, "message": f"Пользователь с {exc.email} уже существует"}
    )


@app.exception_handler(PerevalExistsException)
async def pereval_exists_handler(request: Request, exc: PerevalExistsException):
    return JSONResponse(
        status_code=400,
        content={"status": 400, "message": "Перевал не найден", "id": f"{exc.id}"}
    )
