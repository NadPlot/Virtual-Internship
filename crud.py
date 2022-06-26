from sqlalchemy.orm import Session
from database import Added, Users, Coords, Level, Foto, Images
from schemas import UsersBase, CoordsBase, LevelBase, FotoBase, AddedRaw


# получить одну запись (перевал) по её id
def get_pereval(db: Session, id: int):
    return db.query(Added).filter(Added.id == id).first()


# получить user по id
def get_user(db: Session, id: int):
    return db.query(Users).filter(Users.id == id).first()


# получить user по email (для проверки есть ли user с таким email)
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


def create_pereval(db: Session, pereval: AddedRaw, user_id: int, coords_id: int, level_id: int):
    new_pereval = Added(
        add_time=pereval.add_time,
        beauty_title=pereval.beauty_title,
        title=pereval.title,
        other_titles=pereval.other_titles,
        connect=pereval.connect,
        user_id=user_id,
        coords_id=coords_id,
        level_id=level_id,
        status="new"
    )
    db.add(new_pereval)
    db.commit()
    return new_pereval


# Добавить id в таблицу связей перевала и изображений
def add_relation(db: Session, pereval_id: int, foto_id: int):
    new_relation = Images(
        pereval_id=pereval_id,
        foto_id=foto_id
    )
    db.add(new_relation)
    db.commit()
    return new_relation
