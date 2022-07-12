from distutils.command.upload import upload
from django.db import models


# Create your models here.
class Article(models.Model):
    pass
    # image = model.ImageField(upload_to='images')


class Category(models.Model):
    pass


class Tag(models.Model):
    pass