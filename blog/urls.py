from django.urls import path
from .views import blog_detail, BlogsListView

app_name = 'blog'

urlpatterns = [
    path('', BlogsListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>', blog_detail, name='blog_detail'),
]