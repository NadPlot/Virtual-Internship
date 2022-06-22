from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine, Added
from fastapi import FastAPI


description = """
На сайте https://pereval.online/ ФСТР ведёт базу горных перевалов, которая пополняется туристами.
Проект ФСТР "Перевал Online" создан специально для горных путешественников.
Вы сможете с лёгкостью собрать информацию по нужным перевалам и вершинам с фотографиями, картами и различной полезной информацией.

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
    return {"message": "REST API FSTR"}


# получить одну запись (перевал) по её id.
@app.get("/submitData/{id}/", response_model=schemas.Added)
def read_added_id(id: int, db: Session = Depends(get_db)):
    added = crud.get_added_id(db, id=id)
    return added
