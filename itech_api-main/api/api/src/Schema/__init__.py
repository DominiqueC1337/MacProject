import datetime
#from __future__ import annotations
from typing import List, Union
from pydantic import BaseModel, Field


class AuthStatus(BaseModel):
	details: str


class Blockzeit(BaseModel):
	id: int
	date_from: datetime.date
	date_to: datetime.date
	days: int

	class Config:
		orm_mode = True


class Error(BaseModel):
	error: str


class Greeting(BaseModel):
	key: int
    
	message: str


class Index(BaseModel):
	message: str
	date: datetime.datetime

class HolidayItem(BaseModel):
    start: str
    end: str
    year: int
    stateCode: str
    name: str
    slug: str


class Holiday(BaseModel):
    __root__: List[HolidayItem]
    
#Neue Klassen für das News-Model 
class NewsItem(BaseModel):
    news_id:int
    news_image: str
    news_date_from: datetime.date
    news_date_to: datetime.date
    news_body: str
 	
    class Config:
        orm_mode = True  

class CreateNewsResponse(BaseModel):
	success: bool        
 

class JWT(BaseModel):
	token: str


class Klasse(BaseModel):
	id: int
	name: str

	class Config:
		orm_mode = True


class KlasseWithBlockzeit(Klasse):
	blockzeiten: list[Blockzeit]

	class Config:
		orm_mode = True

class Mac(BaseModel):
	user_name: str
	password: str
	device_name: str
	device_name_2: str
	mac_address: str
	mac_address_2: str

	class Config:
		orm_mode = True


class Login(BaseModel):
	username: str
	password: str
	code: Union[str, None] | None = None


class Register(BaseModel):
	username: str
	password: str
	email: str


class RegisterResponse(BaseModel):
	success: bool


class User(BaseModel):
	username: str
	ldap_data: object

##### -StandIn- ####
class Result(BaseModel):
    class_: str = Field(..., alias='class')
    hour: str
    time: str
    room: str
    info: str


class Date(BaseModel):
    last_update: str
    week_day: str
    date: int
    results: List[Result]
    next_day: int


class StandIn(BaseModel):
    dates: List[Date]
