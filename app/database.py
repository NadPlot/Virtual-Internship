from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from .config import settings


engine = create_engine(settings.db_url)

# подключение к существующей БД (создается при запуске docker-compose)
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

# Определено в соответствии с таблицами БД
Users = Base.classes.pereval_users
Coords = Base.classes.pereval_coords
Level = Base.classes.pereval_level
Foto = Base.classes.pereval_foto
Added = Base.classes.pereval_added
Areas = Base.classes.pereval_areas
Images = Base.classes.pereval_images
Activities_types = Base.classes.spr_activities_types

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
