from django.core.exceptions import ValidationError
from .models import User


def user_exist(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError('Пользователь с таким именем уже создан')