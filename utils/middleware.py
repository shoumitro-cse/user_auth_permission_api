from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from utils.authentication import TokenAuthentication
from utils.renderers import JSONRenderer
from accounts.models import UserToken


class ValidateAccessTokenMiddleware(MiddlewareMixin):
    def __call__(self, request):
        try:
            if self.verify_access_token(TokenAuthentication.get_authenticate_token(request)):
                return super().__call__(request)
        except KeyError as e:
            pass
        return self.response_render({"token": "Invalid Access Token or expired!"})

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

    @staticmethod
    def response_render(data):
        response = Response(data, status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

