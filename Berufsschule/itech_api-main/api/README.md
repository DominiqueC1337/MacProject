# Softwareabhängigkeiten installieren
Folgende Software muss vorinstalliert sein:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

# Umgebungsvariablen definieren
## ``api.env.example`` nach ``api.env`` kopieren und anpassen
* ``AUTH_TEST`` = Flag ob die LDAB Authentifizierung übersprungen werden soll. In diesem Fall muss als JWT-Token IMMER 'example.token' angegeben werden
* ``DB_DNS`` = Angabe des Verbinungsstrings zur doocker-mariadb. Hier muss ggf. nur der USER und das PASSWORT angepasst werden (gemäß der ``db.env``)
* ``LDAP_HOST`` = Host Adressse des LDAP-Systems (z.B. IP-Adressse)
* ``LDAP_PORT`` = Host Port des LDAP-Systems (z.B. 636 für LDAPS)
* ``LDAP_SSL`` = Flag ob SSL zum verbinden mit dem LDAP-System verwendet werden soll (true/false)
* ``LDAP_BASE_DN`` = Basis DN für Verbindungen
* ``LDAP_BIND_USER`` = Verbindungsinformationen für API-User zum lesen des LDAP-Systems
* ``LDAP_BIND_PASSWORD`` = Passwort für API-user zum lesen des LDAP-Systems
* ``LDAP_USER_DN`` = DN für User die sich an der API anmelden wollen
* ``JWT_SECRET`` = Secret zum verschlüsseln des JWT-Tokens
* ``JWT_EXPIRE`` = Angabe in Sekunden wie lange ein JWT-Token gültig sein soll
* ``VIRTUAL_HOST`` = Domainangabe für NGINX
* ``VIRTUAL_PORT`` = Interner Port der API für nginx mapping
* ``FORWARDED_ALLOW_IPS`` = Erlauben des Durchreichens der Client IP für das Logging


## ``db.env.example`` nach ``db.env`` kopieren und anpassen
* ``MYSQL_ROOT_PASSWORD`` = Passwort des Datenbank root users
* ``MYSQL_DATABASE`` = Name der Datenbank für die API
* ``MYSQL_USER`` = Name des Users der Datenbank über den die API Daten abfragen kann
* ``MYSQL_PASSWORD`` = Passwort des Users der Datenbank über den die API Daten abfragen kann

# Dockerpfade in der ``docker-compose.yml``
* SSL-Zertifikate werden im angebenen Ordner hinterlegt werden (services > web > volumes)
* Damit die Datenbank keinen Datenverlust durch beenden oder löschen des Containers erfährt, so ist ein Mapping anzugeben (services > db > volumes)
# Starten
Zum starten der Software folgenden Befehl in die Kommandozeile eingeben:
```bash
docker-compose up --build --detach
```  

Mit dem zusatzparameter ``--detach`` kann die Applikation als Dienst im Hintergrund gestartet werden.
Weiteres dazu unter folgendem link: [`docker-compose up`](https://docs.docker.com/compose/reference/up/)

# Stoppen und Beenden
Zum stoppen der Software folgenden Befehl in die Kommandozeile eingeben:
```bash
docker stop [CONTAINERNAME]
``` 
Als CONTAINERNAME muss die ID des Containers angegeben werden. Diese lässt sich wie folgt auslesen:
```bash
docker ps
``` 
Zum löschen des Container wird folgender Befehler verwendet:
```bash
docker-compose down
``` 
# Löschen und Bereinigen
Müssen alle Daten und Docker Images komplett entfernt werden, so müssen die in der ``docker-compose.yml`` gemappten Verzeichnise manuell gelöscht werden. Um die Container komplett zu entfernen muss folgender Befehl in die Konsole eingegeben werden:
```bash
docker system prune --volumes -af
``` 
