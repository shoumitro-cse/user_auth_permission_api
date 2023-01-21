from django.contrib.auth.models import Permission

from accounts.models import User
from utils.serializers import PermissionModelSerializer
from rest_framework import serializers


class UserSerializer(PermissionModelSerializer):
    permission_fields = []

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "user_type", "mobile", "address"]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "name", "content_type", "codename"]


class UserPermissionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)