from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from accounts.models import UserToken
from django.utils import timezone


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'

    """
    A custom token model may be used, but must have the following properties.

    * access_token -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        return self.authenticate_credentials(self.get_authenticate_token(request))

    @staticmethod
    def get_authenticate_token(request):
        keyword = "Token"
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return token

    @staticmethod
    def authenticate_credentials(access_token):
        try:
            token = UserToken.objects.get(access_token=access_token)
            if token.access_token_expire_date < timezone.now():
                msg = _('Invalid token or expired.')
                raise exceptions.AuthenticationFailed(msg)
        except UserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword
