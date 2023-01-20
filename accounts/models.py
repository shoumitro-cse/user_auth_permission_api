from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils import timezone
from django.conf import settings
import binascii, os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

ADMIN = 1
STAFF = 2
GENERAL = 3

USER_TYPE_CHOICES = (
    (ADMIN, "ADMIN"),
    (STAFF, "STAFF"),
    (GENERAL, "GENERAL"),
)


class User(AbstractUser):
    """ User class model used to store user data"""
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=GENERAL)
    is_staff = models.BooleanField(default=False)
    mobile = models.CharField(max_length=20, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class LoginUsers(models.Model):
    user = models.OneToOneField(User, related_name="login_user", on_delete=models.CASCADE)
    access_token = models.CharField(max_length=40, blank=True, null=True)
    refresh_token = models.CharField(max_length=40, blank=True, null=True)
    access_token_expire_date = models.DateTimeField(null=True, blank=True)
    refresh_token_expire_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "login user"
        verbose_name_plural = "login users"

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = self.generate_key("access_token")
            self.access_token_expire_date = timezone.now() + settings.ACCESS_TOKEN_LIFETIME
        if not self.refresh_token:
            self.refresh_token = self.generate_key("refresh_token")
            self.refresh_token_expire_date = timezone.now() + settings.REFRESH_TOKEN_LIFETIME
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.access_token)

    @classmethod
    def generate_key(cls, token_field="access_token",
                     token_function=lambda: binascii.hexlify(os.urandom(20)).decode()):
        """
            Generates random tokens until a unique one is found
            :param token_field: a string with the name of the token field to search in the model_class
            :param token_function: a callable that returns a candidate value
            :return: the unique candidate token
        """
        unique_token_found = False
        while not unique_token_found:
            token = token_function()
            # This weird looking construction is a way to pass a value to a field with a dynamic name
            if cls.objects.filter(**{token_field: token}).count() is 0:
                unique_token_found = True
        return token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_login_token(sender, instance=None, created=False, **kwargs):
    if created:
        LoginUsers.objects.create(user=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_login_token(sender, instance=None, **kwargs):
    LoginUsers.objects.filter(user=instance).delete()
