#!/bin/bash
export SECRET_KEY=django-insecure-d6^m8g0c@ct^d8!os+1c8nw5_$+wl@@yk_+9iuo*ssm5!^1@lr
export DJANGO_DEBUG=True
export PYTHONUNBUFFERED=TRUE

# OpenID Connect Settings
export OIDC_RP_CLIENT_ID=judge
export OIDC_RP_CLIENT_SECRET=7iDN8MFXGHRoPAGFKpc6nIgyyo4Rplt0
export OIDC_OP_AUTHORIZATION_ENDPOINT=http://127.0.0.1:8080/realms/judge/protocol/openid-connect/auth
export OIDC_OP_TOKEN_ENDPOINT=http://127.0.0.1:8080/realms/judge/protocol/openid-connect/token
export OIDC_OP_USER_ENDPOINT=http://127.0.0.1:8080/realms/judge/protocol/openid-connect/userinfo
export OIDC_OP_JWKS_ENDPOINT=http://127.0.0.1:8080/realms/judge/protocol/openid-connect/certs
export OIDC_OP_LOGOUT_ENDPOINT=http://127.0.0.1:8080/realms/judge/protocol/openid-connect/logout

# Database Settings
export DB_MYSQL_DATABASE=judge
export DB_MYSQL_USERNAME=judge
export DB_MYSQL_PASSWORD=judge
export DB_MYSQL_HOST=localhost
export DB_MYSQL_PORT=3306
