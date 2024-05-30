from users.models import SystemUser, InvitationCode
from common.objects import BaseDTO
from django.contrib.auth.models import User
from django.conf import settings
import requests
import os


def create_user(user_profile, invitation_code):
    code_obj = InvitationCode.get_validate_code(invitation_code)
    if code_obj is not None:
        # Check if username is already taken
        if User.objects.filter(username=user_profile['username']).exists():
            return BaseDTO(False, message="用户名已被占用")
        # Create Django User
        user = User.objects.create_user(username=user_profile['username'], email=user_profile['email'],)
        # Create SystemUser
        SystemUser.objects.create(user=user)
        # Create Keycloak User
        create_keycloak_user(user_profile['username'], user_profile['email'], user_profile['password'])
        # Update InvitationCode
        code_obj.is_used = True
        code_obj.used_by = SystemUser.objects.get(user=user)
        code_obj.save()
    else:
        return BaseDTO(False, message="邀请码不存在或已被使用")


def create_keycloak_user(username, email, password):
    # Step 1: Obtain an Admin Access Token
    token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    token_data = {
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    token_response = requests.post(token_url, data=token_data)
    admin_token = token_response.json().get('access_token')

    # Step 2: Create the User
    users_url = f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users"
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    user_data = {
        'username': username,
        'email': email,
        'enabled': True,
        'emailVerified': True,
        'credentials': [{
            'type': 'password',
            'value': password,
            'temporary': False  # Set to True if you want the user to update the password on first login
        }]
    }
    user_response = requests.post(users_url, json=user_data, headers=headers)
    if user_response.status_code == 201:
        user_id = user_response.json()['id']

        # Step 3: Set the User's Password (if not set during user creation)
        # password_url = f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/reset-password"
        # password_data = {
        #     'type': 'password',
        #     'value': password,
        #     'temporary': False
        # }
        # password_response = requests.put(password_url, json=password_data, headers=headers)

        return 'User created successfully', user_id
    else:
        return 'Failed to create user', None
