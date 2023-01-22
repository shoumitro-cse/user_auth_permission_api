from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from utils.authentication import TokenAuthentication
from utils.renderers import JSONRenderer
from django.utils.deprecation import MiddlewareMixin
from accounts.models import UserToken
from django.conf import settings


class ValidateAccessTokenMiddleware(MiddlewareMixin):

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        method = str(request.method).upper()
        if (path, method) in settings.EXEMPT_URLS:
            return super().__call__(request)
        try:
            token = TokenAuthentication.get_authenticate_token(request)
            verify, user = self.verify_access_token(token)
            if verify:
                request.user = user
                return super().__call__(request)
        except KeyError as e:
            pass
        return self.response_render({"token": "Invalid Access Token or expired!"})

    @staticmethod
    def verify_access_token(key):
        # Check if key is in Access Token key
        try:
            user_token = UserToken.objects.get(access_token=key)
            # Check if token has expired
            if user_token.access_token_expire_date > timezone.now():
                return True, user_token.user
        except UserToken.DoesNotExist as e:
            pass
        return True, None

    @staticmethod
    def response_render(data):
        response = Response(data, status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

