from django.contrib.auth.models import Permission, Group
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


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "name", "content_type", "codename"]


class UserPermissionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)


class GroupSerializer(serializers.Serializer):
    group_name = serializers.CharField(required=True)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)


class AddUserWithGroupSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=False)