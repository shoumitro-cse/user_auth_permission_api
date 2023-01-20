from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from utils.authentication import TokenAuthentication
from utils.renderers import JSONRenderer
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import get_user
from accounts.models import UserToken
from django.conf import LazySettings

settings = LazySettings()


class ValidateAccessTokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print("request.user: ", request.user)
        request.user = SimpleLazyObject(lambda: self.get_token_user(request))
        print("request.user: ", request.user)
        print("is_authenticated: ", request.user.is_authenticated)
        print("------end process_request----")

    def process_response(self, request, response):
        print(response)
        print("------end process_response----")
        return response

    @staticmethod
    def get_token_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        verify, user = ValidateAccessTokenMiddleware.verify_access_token(TokenAuthentication.get_authenticate_token(request))
        if not verify:
            return AnonymousUser()
        return user

    def __call__(self, request):
        print("__call__")
        try:
            if self.verify_access_token(TokenAuthentication.get_authenticate_token(request))[0]:
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

