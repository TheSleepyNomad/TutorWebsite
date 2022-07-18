from django.contrib import admin
from django.urls import path, include

from .views import LandingPageView

app_name = 'landingpage'

urlpatterns = [
    path('', LandingPageView.as_view(), name='index'),
]
