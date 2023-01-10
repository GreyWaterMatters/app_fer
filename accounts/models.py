import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from accounts.managers import CustomUserManager


class AppUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class History(models.Model):
    class Meta:
        app_label = 'accounts'

    name = models.CharField(max_length=100, null=False, blank=False)
    file_path = models.FileField(upload_to='file', max_length=200)
    prediction = models.CharField(max_length=50, null=False, blank=False)
    true_prediction = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(AppUser, to_field='id', on_delete=models.PROTECT)
