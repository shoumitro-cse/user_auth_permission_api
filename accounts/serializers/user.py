from accounts.models import User
from rest_framework import serializers
from utils.serializers import PermissionModelSerializer


class UserSerializer(serializers.ModelSerializer):
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


class PermUserSerializer(UserSerializer, PermissionModelSerializer):
    pass
