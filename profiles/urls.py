from django.urls import path

from django.contrib.auth.views import LoginView
from profiles.views import RegisterView

app_name = 'profiles'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register")
]
