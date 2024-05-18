from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging


logger = logging.getLogger(__name__)


class OidcAuthnBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(OidcAuthnBackend, self).create_user(claims)
        user.username = claims.get('preferred_username', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email', '')
        user.save()
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email', '')
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """Return all users matching the specified username."""
        username = claims.get('preferred_username')
        if not username:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username__iexact=username)

    def verify_claims(self, claims):
        """Overrided: Always returns true."""
        return True
