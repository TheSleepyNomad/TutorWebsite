from django.urls import path
from .views import blog_detail, BlogsListView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    path('', BlogsListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
]