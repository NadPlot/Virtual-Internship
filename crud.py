from sqlalchemy.orm import Session
from database import Added


# получить одну запись (перевал) по её id.
def get_added_id(db: Session, id: int):
    return db.query(Added).filter(Added.id == id).first()
