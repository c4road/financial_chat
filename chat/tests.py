from django.test import TestCase

from django.urls import reverse

from .models import Thread, ChatMessage
from profiles.models import User
# Create your tests here.


class TestingModels(TestCase):

    def setUp(self):

        self.credentials = {
            'username': 'testUser1',
            'email': 'testUser1@gmail.com',
            'password': 'testpass'
        }
        self.user1 = User.objects.create_user(**self.credentials)

    def test_thread_model(self):

        thread = Thread.objects.create(name="test")
        thread_test = Thread.objects.get(name="test")
        self.assertEqual(thread, thread_test)

    def test_chat_message_model(self):

        thread = Thread.objects.create(name="test")
        chat_message = ChatMessage.objects.create(
            thread=thread,
            user=self.user1,
            message="Hola mundo"
        )
        chat_message_test = ChatMessage.objects.get(message="Hola mundo")
        self.assertEqual(chat_message, chat_message_test)


class TestingViews(TestCase):

	def setUp(self):

		self. 
