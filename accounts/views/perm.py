from django.contrib.auth.models import Permission, Group
from rest_framework import generics
from accounts.models import User
from accounts.serializers import PermissionSerializer, UserPermissionSerializer, GroupSerializer, \
    AddUserWithGroupSerializer
from utils.decorators import is_super_user


class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()

    @is_super_user
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserPermissionCreateView(generics.CreateAPIView):
    """
     <div>
       It's used for to add user permission. a sample of curl code are given below. <br/><br/>
            curl -X 'POST' \
              'http://localhost:8000/auth/user-permission-create/' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -H 'Authorization: Token 7f843d73b3d549ba1e5b85a2c1bd1b323d4cd8e6' \
              -d '{
              "user": 2,
              "permissions": [
                21,29
              ]
            }'
     </div>
    """
    serializer_class = UserPermissionSerializer

    @is_super_user
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.data
        user = User.objects.get(id=data.get("user"))
        user.user_permissions.add(*data.get("permissions"))


class GroupCreateView(generics.CreateAPIView):
    """
    <div>
       It's used for to add new group. a sample of curl code are given below. <br/><br/>
            curl -X 'POST' \
              'http://localhost:8000/auth/group-create/' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -H 'X-CSRFTOKEN: PUuMbqultLYoHUMktlbbKHcm3qx7TzJL6eWjxgEepsUQWLNTdMW2vZNhg5AtLYIk' \
              -d '{
              "group_name": "manager",
              "permissions": [
                21,29
              ]
            }'
    </div>
    """
    serializer_class = GroupSerializer

    @is_super_user
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.data
        group = Group.objects.create(name=data.get("group_name"))
        group.permissions.set(data.get("permissions"))


class AddUserWithGroupView(generics.CreateAPIView):
    """
    <div>
       It's used for to add user with group. a sample of curl code are given below. <br/><br/>
            curl -X 'POST' \
              'http://localhost:8000/auth/add-user-with-group/' \
              -H 'accept: application/json' \
              -H 'Content-Type: application/json' \
              -H 'X-CSRFTOKEN: fVFw5hgthYhem4QtYrX1iImFLWhyfLxAwf73r7qmdFdGBVR2ISIS30XAYBkU7aw9' \
              -d '{
              "user": 2,
              "group": 1
            }'
    </div>
    """
    serializer_class = AddUserWithGroupSerializer

    @is_super_user
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.data
        user = User.objects.get(id=data.get("user"))
        user.groups.add(data.get("group"))



