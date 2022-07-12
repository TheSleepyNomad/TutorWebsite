from django.urls import path
from .views import blog_list, blog_detail

app_name = 'blog'

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('blog_detail/', blog_detail, name='blog_detail'),
]