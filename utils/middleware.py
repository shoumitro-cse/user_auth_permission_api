from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from utils.renderers import JSONRenderer
from accounts.models import UserToken
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class ValidateAccessTokenMiddleware(MiddlewareMixin):
    def __call__(self, request):
        try:
            if self.verify_access_token(self.get_authenticate_token(request)):
                return super().__call__(request)
        except KeyError as e:
            pass
        return self.response_render({"token": "Invalid Access Token"})

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
    def response_render(data):
        response = Response(data, status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    @staticmethod
    def verify_access_token(key):
        # Check if key is in Access Token key
        verify = False
        try:
            user_token = UserToken.objects.get(access_token=key)
            # Check if token has expired
            if user_token.access_token_expire_date > timezone.now():
                verify = True
        except UserToken.DoesNotExist as e:
            pass
        return verify

