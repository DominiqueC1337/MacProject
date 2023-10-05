from datetime import datetime
from sqlalchemy.orm import Session
from Model import LoginLog

def create(database: Session, username: str, event: str, ip: str):
    loginlog = LoginLog()
    loginlog.username = username
    loginlog.event = event
    loginlog.ip = ip
    loginlog.timestamp = datetime.now()
    database.add(loginlog)
    database.commit()
    return
