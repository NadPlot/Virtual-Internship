from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.database import Added, Users, Coords, Level, Foto, Images
from app.schemas import UsersBase, CoordsBase, LevelBase, FotoBase, AddedRaw, AddedRead
from app.exceptions import PerevalExistsException


# получить одну запись (перевал) по её id
def get_pereval(db: Session, id: int):
    # получаем данные о перевале
    pereval = db.query(Added).filter(Added.id == id).first()
    if not pereval:
        raise PerevalExistsException(id=id)
    # получаем данные о пользователе
    user = db.query(Users).filter(Users.id == pereval.user_id).first()
    # получаем данные о координатах
    coords = db.query(Coords).filter(Coords.id == pereval.coords_id).first()
    # получаем данные об уровнях
    level = db.query(Level).filter(Level.id == pereval.level_id).first()
    result = jsonable_encoder(pereval)
    result['user'] = jsonable_encoder(user)
    result['coords'] = jsonable_encoder(coords)
    result['level'] = jsonable_encoder(level)
    return result


# получить данные о перевалах по почте user
def get_pereval_by_user_email(db: Session, email: str):
    # получить данные о пользователе
    get_user = db.query(Users).filter(Users.email == email).first()
    # получить перевалы
    get_all_pereval = db.query(Added).filter(Added.user_id == get_user.id).all()
    # добавляем в список все полученные перевалы
    list = [jsonable_encoder(pereval) for pereval in get_all_pereval]
    pereval = {"pereval": list}
    return pereval


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


# редактирование перевала
def update_pereval(db: Session, pereval: AddedRaw, pereval_id: int):
    # получить перевал по id
    db_pereval = db.query(Added).filter(Added.id == pereval_id).first()

    # изменение значения полей таблицы pereval_added
    db_pereval.beauty_title = pereval.beauty_title
    db_pereval.title = pereval.title
    db_pereval.other_titles = pereval.other_titles
    db_pereval.connect = pereval.connect

    # получить координаты
    db_coords = db.query(Coords).filter(Coords.id == db_pereval.coords_id).first()
    # изменение значений координат таблица pereval_coords
    db_coords.latitude = pereval.coords.latitude
    db_coords.longitude = pereval.coords.longitude
    db_coords.height = pereval.coords.height

    # получить уровень
    db_level = db.query(Level).filter(Level.id == db_pereval.level_id).first()
    # изменение значение уровней таблица pereval_level
    db_level.winter = pereval.level.winter
    db_level.summer = pereval.level.summer
    db_level.autumn = pereval.level.autumn
    db_level.spring = pereval.level.spring

    db.add(db_pereval)
    db.add(db_coords)
    db.add(db_level)
    db.commit()
    return db_pereval.id
