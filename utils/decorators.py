from rest_framework.response import Response
from rest_framework import status
from accounts.models import ADMIN


# for get, retrieve, post, put, patch, partial_update, update, delete, destroy method of a view
def has_access_perm(param):
    def decorator(view_func):
        def wrapper(view_obj, request=None, *args, **kwargs):
            try:
                request = view_obj.request or request
                if not request:
                    return get_response("User doesn't exists!")
                if not request.user.is_authenticated or not request.user.has_perm(param):
                    return get_response("Permission's not allowed.")
            except Exception as e:
                return get_response("Permission's not allowed.")
            return view_func(view_obj, request, *args, **kwargs)
        return wrapper
    return decorator


# for get, post, put, patch, delete
def is_super_user(view_func):
    def wrapper(view_obj, request, *args, **kwargs):
        try:
            request = view_obj.request or request
            user_obj = request.user
        except Exception as e:
            return get_response("User doesn't exists!")
        if not user_obj.is_superuser or not user_obj.user_type == ADMIN:
            return get_response("Permission's not allowed. The user must be super permission.")
        return view_func(view_obj, request, *args, **kwargs)
    return wrapper


def get_response(message="Invalid user or permission's not allowed"):
    msg = {
        "success": False,
        "error": message
    }
    return Response(msg, status.HTTP_400_BAD_REQUEST)


# for get, post, put, patch, delete
def is_authenticated_user(function):
    def wrapper(obj, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return get_response()
        return function(obj, request, *args, **kwargs)
    return wrapper


# for get, post, put, patch, delete
def is_staff_user(function):
    def wrapper(obj, request, *args, **kwargs):
        if not request.user.is_staff:
            return get_response()
        return function(obj, request, *args, **kwargs)
    return wrapper
