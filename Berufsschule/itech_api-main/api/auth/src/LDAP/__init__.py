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


def authorize(username: str, password: str):
    user = search_user(username)

    if user is None:
        return None

    if getenv("LDAP_ITECH_PROD").lower() in ['true', '1', 'y', 'yes']:
        connection_user = f"{user['distinguishedName']}"
    else:
        connection_user = f"{getenv('LDAP_USER_DN')}={username},{getenv('LDAP_BASE_DN')}"

    connection = Connection(
        server=get_server(),
        authentication="SIMPLE",
        user=connection_user,
        password=password,
        read_only=True
    )

    if not connection.bind():
        return None
        
    return user


def search_user(username: str, connection=None):
    if connection is None:
        try:
            connection=get_bind()

            if connection is None:
                print('LDAP connection not possible')
                return None
        except BaseException as err:
            print(err)
            return None

    connection.search(search_base=getenv("LDAP_BASE_DN"),
                      search_filter=f"(&(objectCategory=user)(objectClass=user)(userPrincipalName={username}*))",
                      attributes=ALL_ATTRIBUTES)
    
    if len(connection.response) < 1:
        return None

    if getenv("LDAP_ITECH_PROD").lower() in ['true', '1', 'y', 'yes']:
        return connection.response[0]["attributes"]

    return connection.response[0]
