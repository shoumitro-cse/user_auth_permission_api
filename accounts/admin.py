from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from accounts.models import User, UserToken


admin.site.register(User)
admin.site.register(UserToken)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(Session)


