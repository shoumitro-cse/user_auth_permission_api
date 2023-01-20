from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializer
from utils.decorators import is_super_user, is_authenticated_user, is_staff_user


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
    serializer_class = UserSerializer
    # permission_classes = [AllowAny, ]
    queryset = User.objects.all().order_by("id")

    @is_authenticated_user
    @is_staff_user
    @is_super_user
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

    # permission_classes = [IsAuthenticated, ]
    # permission_classes = [AllowAny, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
