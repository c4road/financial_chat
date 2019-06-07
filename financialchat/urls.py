# from django.contrib import admin
# from django.urls import path

# from django.contrib.auth.views import LoginView
# from profiles.views import RegisterView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('login/', LoginView.as_view(), name="login"),
#     path('register/', RegisterView.as_view(), name="register")
# ]

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include('chat.urls', namespace='chat')),
    path('', include('profiles.urls', namespace='profiles')),
]

