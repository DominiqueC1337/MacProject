import uvicorn
from os import remove
from starlette.requests import Request
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends, FastAPI, status
from Database import DatabaseSession
from Schema import Error, Index, Login, LoginResponse, Register, RegisterResponse, UserResponse
from crud import Error as CrudError, LoginLog as CrudLoginLog, User as CrudUser
from LDAP import authorize, search_user
from auth import check_2fa, create_2fa_secret, create_2fa_str, create_qr_code
from Email import send_mail
from fastapi.middleware.cors import CORSMiddleware

api_description = """
Describe your API with **Markdown** here
"""

app = FastAPI(
    title="ITECH Auth API",
    description=api_description,
    version="1.0.0"
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

def get_database():
    database = DatabaseSession()
    try:
        yield database
    finally:
        database.close()


@app.get("/", response_model=Index)
async def index():
    return {"message": "Herzlich Willkommen an der ITECH", "date": datetime.today()}


@app.post("/register", response_model=RegisterResponse, responses={403: {"model": Error}})
async def post_register(credentials: Register, request: Request, database: Session = Depends(get_database)):
    try:
        user = authorize(credentials.username, credentials.password)

        if user is None:
            CrudLoginLog.create(database, credentials.username, 'register failed', request.client.host)
            return { 'success': False }

        db_user = CrudUser.get(database, credentials.username)

        if db_user is None:
            secret = create_2fa_secret()
            CrudUser.create(database, credentials.username, credentials.email, secret)
            qr_str = create_2fa_str(credentials.username, secret)
            img_filename = create_qr_code(qr_str)
            send_mail(credentials.email, "ITECH 2FA", "Hallo, nachfolgenden erhalten Sie den QR-Code zum Einlesen in eine Authenticator App ihrer Wahl. In ihrer Authenticator App wird im Anschluss der Code generiert, der für die Zwei-Faktor-Authentisierung bei der ITECH-API benötigt wird.", [img_filename])
            remove(img_filename)
            CrudLoginLog.create(database, credentials.username, 'register success', request.client.host)
            return { 'success': True }

        CrudLoginLog.create(database, credentials.username, 'register failed (user already exists)', request.client.host)
        return { 'success': False }

    except BaseException as err:
        CrudLoginLog.create(database, credentials.username, 'register error (' + err.__str__() + ')', request.client.host)
        print (err)
        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)


@app.post("/login", response_model=LoginResponse, responses={403: {"model": Error}})
async def post_login(credentials: Login, request: Request, database: Session = Depends(get_database)):
    try:
        user = authorize(credentials.username, credentials.password)

        if user is not None and CrudUser.is_active(database, credentials.username):
            db_user = CrudUser.get(database, credentials.username)
            # check 2FA
            if check_2fa(database, credentials.username, credentials.code):
                CrudUser.update_last_login(database, db_user)
                CrudLoginLog.create(database, credentials.username, 'login success', request.client.host)
                return {
                    'success': True
                }

            CrudLoginLog.create(database, credentials.username, 'login failed (2fa failed)', request.client.host)
            return {
                'success': False
            }

        elif user is not None and CrudUser.is_pending(database, credentials.username):
            db_user = CrudUser.get(database, credentials.username)
            # check 2FA
            if check_2fa(database, credentials.username, credentials.code):
                CrudUser.update_status(database, db_user, 1)
                CrudUser.update_last_login(database, db_user)
                CrudLoginLog.create(database, credentials.username, 'login success', request.client.host)
                return {
                    'success': True
                }

            CrudLoginLog.create(database, credentials.username, 'login failed (2fa failed)', request.client.host)
            return {
                'success': False
            }

        CrudLoginLog.create(database, credentials.username, 'login failed', request.client.host)
        return {
            'success': False
        }
    except BaseException as err:
        CrudLoginLog.create(database, credentials.username, 'login error (' + err.__str__() + ')', request.client.host)
        print (err)
        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)


@app.get("/user/{username}", response_model=UserResponse, responses={404: {"model": Error}})
async def get_user(username: str):
    try:
        user = search_user(username)
        #print (str(user))
        ustr = str(user)
        uarray = ustr.split("'distinguishedName':" )
        #print (uarray[1])
        ua = uarray[1].split(", 'instanceType'" )
        print (ua[0])
        return {
                'dn': ua[0]
                #'dn': user['raw_dn'].decode('utf-8')
        }

    except BaseException as err:
        print(err)
        return CrudError.generic_error(status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    uvicorn.run("main:app",
        host='0.0.0.0',
        log_config="/app/logging.yaml",
        port=8080,
        reload = True,
        server_header = False
    )
