from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from utils.renderers import JSONRenderer
from accounts.models import UserToken


class ValidateAccessTokenMiddleware(MiddlewareMixin):
    def __call__(self, request):
        try:
            # auth_method, token = get_authorization_header(request)
            auth_method, token = request.META['HTTP_AUTHORIZATION'].split(' ')
            if self.verify_access_token(token):
                return super().__call__(request)
        except KeyError as e:
            pass
        return self.response_render({"token": "Invalid Access Token"})

    @staticmethod
    def response_render(data):
        response = Response(data, status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    @staticmethod
    def verify_access_token(token):
        # Check if key is in AccessToken key
        verify = True
        try:
            login_user = UserToken.objects.get(access_token=token)
            # Check if token has expired
            if login_user.access_token_expire_date < timezone.now():
                verify = False
        except UserToken.DoesNotExist as e:
            pass
        return verify

