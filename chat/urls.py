from django.urls import path, re_path


from .views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view(), name="room-list"),
    re_path(r"^(?P<pk>\d+)", ThreadView.as_view(), name='room'),
]
