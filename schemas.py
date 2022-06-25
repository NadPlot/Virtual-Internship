import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int
    email: str
    phone: Optional[int] = None
    fam: Optional[str] = None
    name: Optional[str] = None
    otc: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


class CoordsBase(BaseModel):
    id: int
    latitude: str
    longitude: str
    height: str


class CoordsCreate(CoordsBase):
    pass


class Coords(CoordsBase):
    id: int

    class Config:
        orm_mode = True


class LevelBase(BaseModel):
    id: int
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class LevelCreate(LevelBase):
    pass


class Level(LevelBase):
    id: int
    
    class Config:
        orm_mode = True


class AddedBase(BaseModel):
    add_time: datetime.datetime
    beauty_title: str
    title: str
    other_titles: str
    connect: Optional[str]
    user_id: int
    coords_id: int
    level_id: int
    status: Optional[str] = None


class AddedCreate(AddedBase):
    pass


class Added(AddedBase):
    id: int
    user_id: int
    coords_id: int
    level_id: int

    class Config:
        orm_mode = True


class ImagesBase(BaseModel):
    id: int
    pereval_id: int
    foto_id: int


class ImgesCreate(ImagesBase):
    pass


class Images(ImagesBase):
    id: int
    pereval_id: Added = Field()


class FotoBase(BaseModel):
    id: int
    date_added: datetime.datetime
    img: Optional[bytes] = None


class ImagesCreate(ImagesBase):
    pass


class Images(ImagesBase):
    id: int

    class Config:
        orm_mode = True
