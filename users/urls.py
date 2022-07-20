from django.urls import path
from users.views import login_view, registration_view
app_name = 'users'

urlpatterns = [
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
]