# Start dev environment

python3.12 -m venv .venv
source .venv/bin/activate
source env/env_qa.sh
python manage.py migrate
python manage.py runserver

# Set up Keycloak
unzip keycloak-24.0.4.zip

./bin/kc.sh start-dev

Configurations:
see images in docs/


# Postman Get access token:
POST http://127.0.0.1:8080/realms/judge/protocol/openid-connect/token
username:serenity
password:123456
client_secret:7iDN8MFXGHRoPAGFKpc6nIgyyo4Rplt0
client_id:judge
grant_type:password

