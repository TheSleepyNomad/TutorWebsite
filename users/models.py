from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class User(AbstractUser):
#     image = models.ImageField(
#         upload_to='images/avatars',
#         blank=True,
#         verbose_name='Аватар пользователя',
#     )
#     phone = models.CharField(
#         max_length=20,
#         blank=True,
#         verbose_name='телефон',
#     )
#     patronymic = models.CharField(
#         max_length=30,
#         blank=True,
#         verbose_name='Отчество',
#     )

#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = "Пользователи"