from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from accounts.models import User, UserToken
from accounts.serializers import PasswordResetSerializer
from accounts.serializers.auth import SigninSerializer
import jwt


class SigninView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user_list_obj = User.objects.filter(username=username)
            if user_list_obj.exists():
                username = user_list_obj.first().username
                user = authenticate(request, username=username, password=password)
                if user:
                    return Response(self.get_user_token(user), status.HTTP_200_OK)
        return Response({"message": "Wrong Credentials"}, status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_user_token(user):
        if hasattr(user, "user_token"):
            user_token = user.user_token
            if user_token.access_token_expire_date < timezone.now():
                user_token.access_token_expire_date = timezone.now() + settings.ACCESS_TOKEN_LIFETIME
            if user_token.refresh_token_expire_date < timezone.now():
                user_token.refresh_token_expire_date = timezone.now() + settings.REFRESH_TOKEN_LIFETIME
            user_token.save()
        else:
            user_token = UserToken.objects.create(user=user)
        return {
            "refresh_token": user_token.refresh_token,
            "access_token": user_token.access_token,
        }


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.user_token.delete()
        except UserToken.DoesNotExist as e:
            return Response({"status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            self.send_to_email(request, email)
        return Response({"status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

    @staticmethod
    def send_to_email(request, email):
        user = request.user
        expire = timezone.now() + timezone.timedelta(minutes=5)
        data = {
            'user': user.email,
            'email': email,
            'exp': expire
        }
        token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
        domain = "http://localhost:8000"
        message = f"Dear {user.username},<br> Forgot your password. " \
                  f"We received a request to reset the password of your account.<br/>" \
                  f"To reset your password please click here<br>" \
                  f"<a href='{domain}/confirm-reset-password/{token}/'>Click Here</a>"
        mail_subject = f'Please confirm your reset password.'

        # send_mail(mail_subject, message, settings.FROM_EMAIL_MAIN, [email, ],
        #           html_message=message, fail_silently=False, )
        print(message)
