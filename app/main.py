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
    "method GET by id": "/pereval/{id} - получить данные о перевале по id",
    "method POST": "/submitData/ - отправить данные о перевале (принимает JSON)",
    "method GET by email": "submitData/email/{email] - по email получить список отправленных перевалов",
    "method PATCH": "submitData/{id} - отредактировать запись о перевале, принимает JSON"
}


# получить одну запись (перевал) по id.
@app.get("/pereval/{id}/", response_model=schemas.AddedRead)
def read_pereval(id: int, db: Session = Depends(get_db)):
    pereval = crud.get_pereval(db, id=id)
    if not pereval:
        raise PerevalExistsException(id)
    return pereval


# получить перевал(ы) по почте пользователя
@app.get("/submitData/email/{email}", response_model=schemas.AddedList)
def get_pereval_list_by_user_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise EmailNotExistsException(email=email)
    list = crud.get_pereval_by_user_email(db, email=email)
    return list


# отправить данные о перевале
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


# отредактировать отправленные данные, если статус new
@app.patch("/submitData/{id}", response_model=schemas.AddedBase)
def edit_pereval(id: int, pereval: schemas.AddedRaw, db: Session = Depends(get_db)):
    get_pereval = crud.get_pereval(db, id=id)  # получаем перевал по id из БД
    if not get_pereval:
        raise PerevalExistsException(id)
    if get_pereval['status'] == "new":  # проверяем статус перевала
        crud.update_pereval(db, pereval, id)
    else:
        list_status = {
            "new": "новый",
            "pending": "в работе",
            "accepted": "принят",
            "rejected": "отклонен"
        }
        status = get_pereval['status']  # получаем статус, например new
        for keys in list_status:
            if keys == status:
                st = list_status.get(f"{status}")
                return JSONResponse(status_code=400, content={"state": 0, "message": f"Невозможно внести изменения. Статус перевала: {st}"})
    return JSONResponse(status_code=200, content={"state": 1, "message": "Отправлено успешно"})


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
