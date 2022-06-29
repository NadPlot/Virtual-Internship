from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
from exceptions import PerevalExistsException, EmailNotExistsException


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


# получить одну запись (перевал) по id.
@app.get("/pereval/{id}/", response_model=schemas.AddedRead)
def read_pereval(id: int, db: Session = Depends(get_db)):
    return crud.get_pereval(db, id=id)


# получить перевал(ы) по почте пользователя (НЕ ГОТОВ)
@app.get("/submitData/{email}", response_model=schemas.AddedList)
def get_pereval_list_by_user_email(email: str, db: Session = Depends(get_db)):
    list = crud.get_pereval_by_user_email(db, email=email)
    if list["user"] == None:
        raise EmailNotExistsException(email=email)
    return list


# отправить данные о перевале (ДОБАВИТЬ ПРОВЕРКУ ПОДКЛ К БД)
@app.post("/submitData/", response_model=schemas.AddedBase)
def add_pereval(raw_data: schemas.AddedRaw, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=raw_data.user.email)
    if db_user:
        user = db_user.id
    else:
        user = crud.create_user(db, user=raw_data.user)

    coords = crud.create_coords(db, coords=raw_data.coords)
    level = crud.create_level(db, level=raw_data.level)
    foto = crud.add_foto(db, foto=raw_data.images)
    pereval = crud.create_pereval(db, raw_data, user, coords, level)
    images = crud.add_relation(db, pereval.id, foto)
    return JSONResponse(status_code=200, content={"status": 200, "message": "Отправлено успешно", "id": pereval.id})


@app.exception_handler(PerevalExistsException)
async def pereval_exists_handler(request: Request, exc: PerevalExistsException):
    return JSONResponse(
        status_code=400,
        content={"status": 400, "message": "Перевал не найден", "id": f"{exc.id}"}
    )


@app.exception_handler(EmailNotExistsException)
async def email_not_exists_handler(request: Request, exc: EmailNotExistsException):
    return JSONResponse(
        status_code=400,
        content={"status": 400, "message": "Пользователь с данным email не зарегестрирован"}
    )
