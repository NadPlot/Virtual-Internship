from sqlalchemy.orm import Session
from database import Added, Users
from schemas import UsersBase


# получить одну запись (перевал) по её id
def get_pereval(db: Session, id: int):
    return db.query(Added).filter(Added.id == id).first()

# получить user по id
def get_user(db: Session, id: int):
    return db.query(Users).filter(Users.id == id).first()

# получить user по email
def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

# функции для POST/submitData/
# Создать пользователя
def create_user(db: Session, user: UsersBase):
    new_user = Users(**user.dict())

    db.add(new_user)
    db.commit()
    return new_user
