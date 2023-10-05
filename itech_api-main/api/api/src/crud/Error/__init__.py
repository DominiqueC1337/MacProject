import http
from fastapi.responses import JSONResponse


def generic_error(status_code):
    return JSONResponse(status_code=status_code, content={
        "error": http.HTTPStatus(status_code).phrase
    })


def error(status_code, message):
    return JSONResponse(status_code=status_code, content={
        "error": message
    })
