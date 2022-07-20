from django.contrib import admin
from django import forms
from .models import Article, Category, Tag, Gallery
# Register your models here.

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = '__all__'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'prev_text', 'entry_image', 'text', 'category')
    form = ArticleAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass