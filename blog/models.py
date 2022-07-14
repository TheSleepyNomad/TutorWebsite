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
    prev_text = models.TextField()
    entry_image = models.ImageField(upload_to='images/banners')
    text = models.TextField() # Хранит в себе HTML разметку с текстом
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey()

    class Meta:
        get_latest_by = "-created_at"

    def __str__(self) -> str:
        return f'Статья - {self.title}'


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Article, on_delete=models.CASCADE)
#     text = models.TextField()
#     created = models.DateTimeField(default=timezone.now, null=True)
#     moderation = models.BooleanField(default=False)

#     def __str__(self):
#         return self.text