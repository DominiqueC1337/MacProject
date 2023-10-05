from sqlalchemy import Column, DateTime, Integer, String
from Database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mfa_secret = Column(String, nullable=False)
    status = Column(Integer, nullable=False, comment="0 = Inaktiv | 1 = Aktiv | 2 = Gesperrt")
    created_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<User(username='%s' email='%s', mfa_secret='%s', status=%d)>" % (self.username, self.email, self.mfa_secret, self.status)


class LoginLog(Base):
    __tablename__ = 'login_log'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    event = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<LoginLog(username='%s', event='%s', ip='%s', timestamp='%s')>" % (self.username, self.event, self.ip, self.timestamp)
