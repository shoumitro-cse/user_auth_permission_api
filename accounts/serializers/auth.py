from rest_framework import serializers

from accounts.models import User


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
