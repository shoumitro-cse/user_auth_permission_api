from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, LoginUsers


admin.site.register(User)
admin.site.register(LoginUsers)
admin.site.register(Permission)
admin.site.register(ContentType)


