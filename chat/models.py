from django.db import models
from django.conf import settings


class Thread(models.Model):

    name = models.CharField('Room name', max_length=70,
                            null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
