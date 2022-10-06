from django.db import models
from django.contrib.auth.models import AbstractUser


def get_avatar_path(instance, filename):
    return "avatars/%s" % (filename)


class User(AbstractUser):
    avatar = models.ImageField(verbose_name="Аватар", upload_to=get_avatar_path, blank=True)
    description = models.CharField(verbose_name="О себе", max_length=600, blank=True)
