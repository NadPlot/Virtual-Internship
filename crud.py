from sqlalchemy.orm import Session
from database import Added, Users


# получить одну запись (перевал) по её id.
def get_pereval(db: Session, id: int):
    return db.query(Added).filter(Added.id == id).first()
