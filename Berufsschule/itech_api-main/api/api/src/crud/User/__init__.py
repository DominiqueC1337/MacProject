from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from Model import User

def create(database: Session, username: str, email: str, secret: str):
    user = User()
    user.username = username
    user.email = email
    user.mfa_secret = secret
    user.status = 0
    user.created_at = datetime.now()
    database.add(user)
    database.commit()
    return

def update_secret(database: Session, user: User, secret: str):
    user.mfa_secret = secret
    # database.add(user)
    database.commit()
    return

def update_status(database: Session, user: User, status: int):
    user.status = status
    # database.add(user)
    database.commit()
    return

def update_last_login(database: Session, user: User):
    user.last_login = datetime.now()
    # database.add(user)
    database.commit()
    return

def get(database: Session, username: str):
    return database.query(User).filter(User.username == username).first()

def is_active(database: Session, username: str):
    user = get(database, username)

    if user is None:
        return False

    return user.status == 1

def is_pending(database: Session, username: str):
    user = get(database, username)

    if user is None:
        return False

    return user.status == 0
