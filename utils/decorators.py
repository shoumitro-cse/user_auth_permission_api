from rest_framework.response import Response
from rest_framework import status

response_msg = {
    "success": False,
    "error": "Invalid user or permission's not allowed"
}

def has_access_perm(param):
    def decorator(view_func):
        def wrapper(obj, request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.has_perm(param):
                return Response(response_msg, status.HTTP_400_BAD_REQUEST)
            return view_func(obj, request, *args, **kwargs)
        return wrapper
    return decorator


def is_super_user(function):
    def wrapper(obj, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(response_msg, status.HTTP_400_BAD_REQUEST)
        return function(obj, request, *args, **kwargs)
    return wrapper


def is_authenticated_user(function):
    def wrapper(obj, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(response_msg, status.HTTP_400_BAD_REQUEST)
        return function(obj, request, *args, **kwargs)
    return wrapper


def is_staff_user(function):
    def wrapper(obj, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(response_msg, status.HTTP_400_BAD_REQUEST)
        return function(obj, request, *args, **kwargs)
    return wrapper
