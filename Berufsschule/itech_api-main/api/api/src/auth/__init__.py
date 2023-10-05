import jwt
import requests
from os import getenv
from starlette.requests import Request
from time import time
from typing import Dict
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def register(username: str, password: str, email: str, request: Request):
    payload = { "username": username, "password": password, "email": email }
    header = { "X-Forwarded-For": request.client.host }
    request = requests.post("http://auth:8080/register", json=payload, headers=header)
    return request.json()

def authorize(username: str, password: str, code: str, request: Request):
    payload = { "username": username, "password": password, "code": code }
    header = { "X-Forwarded-For": request.client.host }
    request = requests.post(getenv("AUTH_API_URL")+ "/login", json=payload, headers=header)
    return request.json()

def getDN(username: str):
    request = requests.get(getenv("AUTH_API_URL")+ "/user/" + username)
    return request.json()

def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time() + int(getenv("JWT_EXPIRE"))
    }
    token = jwt.encode(payload, getenv("JWT_SECRET"), algorithm="HS256")

    return {
        "token": token
    }


def decode_jwt(token: str):
    try:
        if getenv("AUTH_TEST").lower() in ['true', '1', 'y', 'yes'] and token == "example.token":
            decoded_token = {"expires": time()+3600}
        else:
            decoded_token = jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])
        
        return decoded_token if decoded_token["expires"] >= time() else None
    except BaseException as err:
        print (err)
        return None


def verify_jwt(jwtoken: str) -> bool:
    is_token_valid = False
    try:
        if decode_jwt(jwtoken) is not None:
            is_token_valid = True
    except BaseException as err:
        print (err)
        is_token_valid = False

    return is_token_valid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403)
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403)
            return credentials.credentials
        else:
            raise HTTPException(status_code=403)
