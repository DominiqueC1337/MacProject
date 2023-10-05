from sqlalchemy.orm import Session, selectinload
from datetime import datetime, date
from Model import News

def get_all(database: Session):
    return database.query(News).all()
    
def get_all_date(database: Session):
    current = date.today().isoformat()
    return database.query(News).where(News.news_date_from <= current, News.news_date_to >= current).all()
   
def create(image: str, date_from: date, date_to: date, body: str, database: Session):
    news = News()
    news.news_image = image
    news.news_date_from = date_from
    news.news_date_to = date_to
    news.news_body = body
    database.add(news)
    database.commit()
    return

