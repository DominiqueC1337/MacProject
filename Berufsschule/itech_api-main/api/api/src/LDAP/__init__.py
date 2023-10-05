from os import getenv
from ldap3 import ALL, Connection, Server, ALL_ATTRIBUTES


def get_server():
    use_ssl = getenv("LDAP_SSL").lower() in ['true', '1', 'y', 'yes']
    return Server(host=getenv("LDAP_HOST"), port=int(getenv("LDAP_PORT")), use_ssl=use_ssl, get_info=ALL)


def get_bind():
    connection = Connection(
        server=get_server(),
        authentication="SIMPLE",
        user=f"{getenv('LDAP_BIND_USER')}, {getenv('LDAP_BASE_DN')}",
        password=getenv("LDAP_BIND_PASSWORD"),
        read_only=True,
        raise_exceptions=True
    )

    if not connection.bind():
        return None

    return connection

def search_user(username: str, connection=None):
    if connection is None:
        connection=get_bind()

    if connection is None:
        return None

    connection.search(search_base=getenv("LDAP_BASE_DN"),
                      search_filter=f"(&(objectClass=user)({getenv('LDAP_USER_DN')}={username}))",
                      attributes=ALL_ATTRIBUTES)
    
    if len(connection.response) < 1:
        return None

    return connection.response[0]["attributes"]
