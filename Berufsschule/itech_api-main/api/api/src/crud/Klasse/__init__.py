from sqlalchemy.orm import Session, selectinload
from Model import Klasse

def get_all(database: Session):
    return database.query(Klasse).all()

def get(database: Session, klasse: int):
    return database.query(Klasse).filter(Klasse.id == klasse).first()
