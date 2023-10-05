from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table, Text, DateTime
from sqlalchemy.orm import relationship
from Database import Base

klasse_to_blockzeit = Table('klasse_to_blockzeit', Base.metadata,
    Column('klasse_id', ForeignKey('klasse.id'), primary_key=True),
    Column('blockzeit_id', ForeignKey('blockzeit.id'), primary_key=True)
)


class Klasse(Base):
    __tablename__ = 'klasse'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    blockzeiten = relationship(
        "Blockzeit",
        secondary=klasse_to_blockzeit,
        back_populates="klassen")

    def __repr__(self):
        return "<Klasse(name='%s')>" % self.name


class Blockzeit(Base):
    __tablename__ = 'blockzeit'

    id = Column(Integer, primary_key=True)
    date_from = Column(Date)
    date_to = Column(Date)
    days = Column(Integer)
    klassen = relationship(
        "Klasse",
        secondary=klasse_to_blockzeit,
        back_populates="blockzeiten")

    def __repr__(self):
        return "<Blockzeit(date_from='%s', date_to='%s', days='%d')>" % (self.dateFrom, self.dateTo, self.days)
        

#Neues Model für die News
class News(Base):
    __tablename__ = 'news'

    news_id = Column(Integer, primary_key=True)
    news_image = Column(String)
    news_date_from = Column(Date)
    news_date_to = Column(Date)
    news_body = Column(String)     

    def __repr__(self):
        return "<News(news_image='%s')>" % self.news_image

#Neues Model für die Mac-Adressen
class Mac_Address(Base):
    __tablename__ = 'mac_address'

    mac_address = Column(String, primary_key = True)
    user_id = Column(Integer, foreign_key = True)

    def __repr__(self):
        return "<Mac_Address(mac_address='%s', user_id='%d')>" % (self.mac_address, self.user_id)

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
        return "<User(username='%s', email='%s', mfa_secret='%s', status=%d)>" % (self.username, self.email, self.mfa_secret, self.status)
