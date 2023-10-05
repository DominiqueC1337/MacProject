from sqlalchemy.orm import Session
from Model import Mac_Address
from sqlalchemy import delete

def create(database: Session, mac_address: str, id: str, name: str):
    mac = Mac_Address()
    mac.mac_address = mac_address
    mac.user_id = id
    mac.device_name = name
    database.add(mac)
    database.commit()
    return

def delete(database: Session, id: str):
    return database.query(Mac_Address).filter(Mac_Address.user_id == id).delete()



