from django.urls import path
from accounts import views

urlpatterns = [
    #  This URL is used for user registration and to see user lists
    path('user-list-or-register/', views.UserListCreateView.as_view(), name='create_list'),
    # This URL is used for a user to retrieve, partially or fully update and delete
    path('user-retrieve-update-delete/<int:pk>/', views.UserUpdateDeleteDestroyView.as_view(),
         name='user_retrieve_update_delete'),

    #  This URL is used to see permission list
    path('permission-list/', views.PermissionListView.as_view(), name='permission_list'),
    #  This URL is used to add user permission
    path('user-permission-create/', views.UserPermissionCreateView.as_view(), name='user_permission_create'),
    #  This URL is used to add group with permission
    path('group-create/', views.GroupCreateView.as_view(), name='group_create'),
    #  This URL is used to add user with group
    path('add-user-with-group/', views.AddUserWithGroupView.as_view(), name='add_user_with_group'),

    #  This URL is used to login
    path('login/', views.SigninView.as_view(), name='login'),
    #  This URL is used to logout
    path('logout/', views.LogoutView.as_view(), name='logout'),

    #  This URL is used to logout
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
]
