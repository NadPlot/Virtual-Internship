from sqlalchemy.orm import Session
from database import Added, Users, Coords, Level, Foto
from schemas import UsersBase, CoordsBase, LevelBase, FotoBase


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
    return new_user.id


def create_coords(db: Session, coords: CoordsBase):
    new_coords = Coords(**coords.dict())
    db.add(new_coords)
    db.commit()
    return new_coords.id


def create_level(db: Session, level: LevelBase):
    new_level = Level(**level.dict())
    db.add(new_level)
    db.commit()
    return new_level.id


def add_foto(db: Session, foto: FotoBase):
    for image in foto:
        foto = Foto(img=image.data, title=image.title)
    db.add(foto)
    db.commit()
    return foto.id
