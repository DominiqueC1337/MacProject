from datetime import datetime
import pyotp
import qrcode
from crud import User as CrudUser
from sqlalchemy.orm import Session


def check_2fa(database: Session, username: str, code: str) -> bool:
    try:
        user = CrudUser.get(database, username)
        print(user)
        totp = pyotp.TOTP(user.mfa_secret)
        return totp.verify(code)
    except BaseException as err:
        print(err)
        return False


def create_2fa_secret():
    return pyotp.random_base32()


def create_2fa_str(username: str, secret: str):
    return pyotp.TOTP(secret).provisioning_uri(name=f"{username}", issuer_name='ITECH')


def create_2fa(database: Session, username: str, email: str) -> str:
    secret = create_2fa_secret()
    user = CrudUser.get(database, username)
    if user is not None:
        CrudUser.update(database, user, secret)
    else:
        CrudUser.create(database, username, email, secret)
    qr = create_2fa_str(username, secret)
    return qr

def create_qr_code(qr_str: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(qr_str)
    qr.make(fit=True)

    img = qr.make_image()

    filename = str(datetime.now().timestamp()) + ".png"

    img.save("/tmp/" + filename)

    return "/tmp/" + filename
