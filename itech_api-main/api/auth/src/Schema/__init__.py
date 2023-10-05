import datetime
from pydantic import BaseModel
from typing import Union


class AuthStatus(BaseModel):
	details: str


class Error(BaseModel):
	error: str


class Index(BaseModel):
	message: str
	date: datetime.datetime


class LoginResponse(BaseModel):
	success: bool


class Login(BaseModel):
	username: str
	password: str
	code: Union[str, None]


class Register(BaseModel):
	username: str
	password: str
	email: str


class RegisterResponse(BaseModel):
	success: bool


class User(BaseModel):
	username: str
	ldap_data: object


class LoginLog(BaseModel):
	id: int
	username: str
	event: str
	ip: str

	class Config:
		orm_mode = True

class UserResponse(BaseModel):
	dn: str
