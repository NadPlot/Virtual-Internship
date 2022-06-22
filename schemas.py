import datetime
from typing import Optional
from pydantic import BaseModel, Field


# таблица pereval_images
class ImagesBase(BaseModel):
    date_added: datetime.datetime
    img: Optional[bytes] = None


class ImagesCreate(ImagesBase):
    id: int

    class Config:
        orm_mode = True


# для AddedRaw, то что получаем (JSON):
class User(BaseModel):
    id: str
    email: str
    phone: Optional[int] = None
    fam: Optional[str] = None
    name: Optional[str] = None
    otc: Optional[str] = None


class Coords(BaseModel):
    latitude: str
    longitude: str
    height: str


class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class Images(BaseModel):
    sedlo: Optional[list] = None
    Nord: Optional[list] = None
    West: Optional[list] = None
    South: Optional[list] = None
    East: Optional[list] = None

# поля, отправленные в теле запроса (JSON)
class AddedRaw(BaseModel):
    id: int
    beautyTitle: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str]
    add_time: str
    user: User = Field()
    coords: Coords = Field()
    type: Optional[str] = 'pass'
    level: Level = Field()
    images: Optional[Images] = None


# столбец raw_data (table pereval_added)
class RawData(BaseModel):
    pereval_id: int
    beautyTitle: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    user: dict
    coords: dict
    type: str = 'pass'
    level: dict


# MVP1: отправить информацию об объекте на сервер
class AddedBase(BaseModel):
    date_added: datetime.datetime
    raw_data: RawData = Field()
    images: Optional[dict] = None
    status: Optional[str] = None


class AddedCreate(AddedBase):
    id: int


class Added(AddedBase):
    pass

    class Config:
        orm_mode = True