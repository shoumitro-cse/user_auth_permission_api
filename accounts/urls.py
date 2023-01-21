from django.urls import path
from accounts import views

urlpatterns = [
    #  This URL is used for user registration and to see user lists
    path('user-create-list/', views.UserListCreateView.as_view(), name='create_list'),
    # This URL is used for a user to retrieve, partially or fully update and delete
    path('user-retrieve-update-delete/<int:pk>/', views.UserUpdateDeleteDestroyView.as_view(),
         name='user_retrieve_update_delete'),

    #  This URL is used to see permission list
    path('permission-list/', views.PermissionListView.as_view(), name='permission_list'),
    #  This URL is used to add user permission
    path('user-permission-create/', views.UserPermissionCreateView.as_view(), name='user_permission_create'),
]
