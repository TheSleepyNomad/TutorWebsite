from tkinter import CASCADE
from django.db import models
from users.models import Users
from ckeditor.fields import RichTextField

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
    prefix = models.CharField(max_length=100, verbose_name='Наименование файла')
    image = models.ImageField(upload_to='images')

    def __str__(self) -> str:
        return f'Обложка статьи - {self.image}' if self.prefix == 'entry' else f'Картинка в статье - {self.image}'


class Article(models.Model):
    title = models.CharField(max_length=210, verbose_name='Заголовок')
    prev_text = models.TextField() # Хранит в себе HTML разметку с текстом
    entry_image = models.ForeignKey(Gallery, related_name='images',on_delete=models.DO_NOTHING)
    text = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "-created_at"

    def __str__(self) -> str:
        return f'Статья - {self.title}'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # Для отключения комментария

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'Comment by {self.user} on {self.article}'
