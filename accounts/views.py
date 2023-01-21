from django.contrib.auth.models import Permission, Group
from rest_framework import generics
from accounts.models import User
from accounts.serializers import PermUserSerializer, PermissionSerializer, UserPermissionSerializer, GroupSerializer, \
    AddUserWithGroupSerializer
from utils.decorators import has_access_perm, is_super_user


class UserListCreateView(generics.ListCreateAPIView):
    """
    <div style='text-align: justify;'>
    This api is to be used to register like john, justin etc person account
    or to see all user lists. register api also open for Non-Authenticated user
    and Only Authenticated admin super will be able to see user lists.<br/>
    when an admin user try to send this request:
    <ul>
        <li> It performs register operation after sending a post request </li>
        <li> It gives a list of user after sending a get request.</li>
    </ul>
    </div>
    """
    serializer_class = PermUserSerializer
    queryset = User.objects.all().order_by("id")

    # @has_access_perm("accounts:view_user")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserUpdateDeleteDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    <div style='text-align: justify;'>
    This API is used to get four HTTP methods functionality
    like get, put, patch, and delete for user crud operation.
    it is only for Authenticated users. <br/>Non-Authenticated users can't access it.
    when an admin user try to send this request:
    <ul>
        <li> It performs an update operation after sending a put request.</li>
        <li> It performs a partial update operation after sending a patch request.</li>
        <li> It performs a delete operation after sending a delete request.</li>
        <li> It gives the user details after sending a get request.</li>
    </ul>
    </div>
    """
    serializer_class = PermUserSerializer
    queryset = User.objects.all()

    @has_access_perm("accounts:delete_user")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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



