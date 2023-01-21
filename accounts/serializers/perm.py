from django.contrib.auth.models import Permission, Group
from accounts.models import User
from rest_framework import serializers


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