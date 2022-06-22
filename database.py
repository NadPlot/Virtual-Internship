import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


FSTR_DB_HOST = os.environ.get('FSTR_DB_HOST')
FSTR_DB_PORT = os.environ.get('FSTR_DB_PORT')
FSTR_DB_LOGIN = os.environ.get('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.environ.get('FSTR_DB_PASS')

DATABASE_URL = f"postgresql://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/HakatonSK"

engine = create_engine(DATABASE_URL)

metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Added = Base.classes.pereval_added
Areas = Base.classes.pereval_areas
Images = Base.classes.pereval_images
Activities_types = Base.classes.spr_activities_types

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
