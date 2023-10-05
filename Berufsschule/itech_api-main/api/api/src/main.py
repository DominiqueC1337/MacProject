import uvicorn
import requests
import json
from starlette.requests import Request
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi import Depends, FastAPI, status
from Database import DatabaseSession
from Schema import AuthStatus, Error, Greeting, Index, JWT, Klasse as SchemaKlasse, KlasseWithBlockzeit, Login, User, Register, RegisterResponse, HolidayItem, Holiday, StandIn, NewsItem, CreateNewsResponse
from Schema import Mac
from crud import User, Mac_Address
from crud import Klasse as CrudKlasse, Error as CrudError, News as CrudNews
from LDAP import search_user
from auth import authorize, JWTBearer, register, sign_jwt, getDN
from os import getenv
from func.standin import getDataForDate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder


classname = ""
api_description = """
Describe your API with **Markdown** here
"""

app = FastAPI(
    title="ITECH",
    description=api_description,
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_database():
    database = DatabaseSession()
    try:
        yield database
    finally:
        database.close()

#---------------------------
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/handler")
async def post_handle(request: Request):
    directions = {
        "reg": post_reg
    }
    data = jsonable_encoder(await request.form())
    tag = data["tag"]
    dt = data
    response = await (directions[tag](dt, request))
    return response

@app.post("/reg")
async def post_reg(credentials: Register, request: Request):
    register_response = register(credentials["username"], credentials["password"], credentials["email"], request)
    print(register_response)
    return {"ok": True}

@app.post("/mac-address")
async def post_mac_address(credentials: Mac, request: Request, database: Session = Depends(get_database)):
    id = User.get(database, credentials.user_name).id
    Mac_Address.delete(database, id)
    if credentials.device_name is not None and credentials.mac_address is not None:
        Mac_Address.create(database, credentials.mac_address, id, credentials.device_name)
    if credentials.device_name_2 is not None and credentials.mac_address_2 is not None:
        Mac_Address.create(database, credentials.mac_address_2, id, credentials.device_name_2)
    return {"ok": True}






#---------------------------

#@app.get("/", response_model=Index)
#async def index():
#    return {"message": "Herzlich Willkommen an der ITECH", "date": datetime.today()}


@app.post("/login", response_model=JWT, responses={403: {"model": Error}})
async def post_login(credentials: Login, request: Request):
    try:
        user = authorize(credentials.username, credentials.password, credentials.code, request)
        if user["success"]:
            return sign_jwt(credentials.username)
        
        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)
    except BaseException as err:
        print(err)
        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)


@app.post("/register", response_model=RegisterResponse, responses={403: {"model": Error}})
async def post_register(credentials: Register, request: Request):
    try:
        register_response = register(credentials.username, credentials.password, credentials.email, request)
        if register_response["success"]:
            return {
                'success': True
            }

        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)
    except BaseException as err:
        print(err)
        return CrudError.generic_error(status.HTTP_403_FORBIDDEN)


@app.get("/authstatus", response_model=AuthStatus, dependencies=[Depends(JWTBearer())])
async def get_authstatus():
    return {
        "details": "Authenticated"
    }


@app.get("/klasse/", response_model=list[SchemaKlasse], dependencies=[Depends(JWTBearer())])
async def get_all_klassen(database: Session = Depends(get_database)):
    return CrudKlasse.get_all(database)


@app.get("/klasse/{klasse}/",
            response_model=KlasseWithBlockzeit,
            dependencies=[Depends(JWTBearer())],
            responses={404: {"model": Error}}
         )
async def get_klasse(klasse: int, database: Session = Depends(get_database)):
    result = CrudKlasse.get(database, klasse)
    if result is None:
        return CrudError.generic_error(status.HTTP_404_NOT_FOUND)
    return result


#@app.get("/user/{username}/",
#            response_model=User,
#            dependencies=[Depends(JWTBearer())],
#            responses={404: {"model": Error}}
#         )
#async def get_user(username: str):
#    user = search_user(username)
#    if user is None:
#        return CrudError.generic_error(status.HTTP_404_NOT_FOUND)
#    return {"username": username, 'ldap_data': user}


@app.post("/greeting", response_model=Greeting, dependencies=[Depends(JWTBearer())])
async def post_greeting(greeting: Greeting):
    return {"message": greeting.message, "key": greeting.key, "value": greeting}


@app.get("/holiday", response_model=Holiday)
async def read_holiday():
    url = "https://ferien-api.de/api/v1/holidays/HH/2023"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

# Endpunkt News    
@app.get("/news", response_model=list[NewsItem])
async def get_all_news(database: Session = Depends(get_database)):
    return CrudNews.get_all_date(database)
    #return [{"news_image": "Test"}, {"news_image": "Test"}]
    
# Endpunkt News erstellen
@app.post("/createnews", response_model=CreateNewsResponse, dependencies=[Depends(JWTBearer())])
async def create_news(username:str, image:str, date_from:date, date_to:date, body:str, database: Session = Depends(get_database)):
    if "TEACHER" in str(getDN(username)):
        CrudNews.create(image, date_from, date_to, body, database)
        return {
                    'success': True
                }
    else:
        return {
                    'success': False
                }

#@app.get("/standin", response_model=Index)
#async def standin():
#      return {"message": "StandIn !!","date": datetime.today() }

@app.get("/standin", response_model=StandIn)
async def standin():

    # Holen und formatieren, des aktuellen Datums (20220819)
    current_date = date.today()
    currentDate = "{}{}{}".format(
        current_date.strftime("%Y"),
        current_date.strftime("%m"),
        current_date.strftime("%d")
    )

    # Daten für Heute und Morgen holen (Wenn es Freitag ist, dann ist Morgen Montag)
    today = getDataForDate(int(currentDate), classname)
    tomorrow = getDataForDate(int(today["next_day"]), classname)
    data = {
        "dates": [today, tomorrow]
    }
    dataStr = json.dumps(data, indent=4)
    return json.loads(dataStr)

###############################
if __name__ == '__main__':
    uvicorn.run("main:app",
        host='0.0.0.0',
        log_config="/home/vagrant/Documents/Berufsschule/itech_api-main/api/api/config/logging.yaml",
        port=8080,
        reload = True,
        server_header = False
    )
