from turtle import update
from unicodedata import category
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование тэга')

    def __str__(self) -> str:
        return self.name


class Gallery(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование файла')
    image = models.ImageField(upload_to='images')
    description = models.TextField(verbose_name='Описание изображения', blank=True)


class Article(models.Model):
    title = models.CharField(max_length=70, verbose_name='Заголовок')
    entry_image = models.ImageField(upload_to='blogs_banners')
    # Хранит в себе HTML разметку с текстом
    text = models.TextField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey()


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Article, on_delete=models.CASCADE)
#     text = models.TextField()
#     created = models.DateTimeField(default=timezone.now, null=True)
#     moderation = models.BooleanField(default=False)

#     def __str__(self):
#         return self.text