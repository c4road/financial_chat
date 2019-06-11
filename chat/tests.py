from django.test import TestCase
from profiles.models import User
from django.test import Client

from .models import Thread, ChatMessage


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

        self.credentials = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'secret',
        }

        self.login_credentials = {
            'email': 'test_user@gmail.com',
            'password': 'secret'
        }

        self.user_1 = User.objects.create_user(**self.credentials)

    def test_room_view(self):

        if self.client.login(**self.login_credentials):

            response = self.client.get('/rooms/')

        self.assertEqual(response.status_code, 200)

    def test_room_view_redirection(self):

        response = self.client.get('/rooms/')

        self.assertEqual(response.status_code, 302)

    def test_create_room(self):

        csrf_client = Client(enforce_csrf_checks=False)

        if csrf_client.login(**self.login_credentials):

            response = csrf_client.post(
                '/rooms/', {'name': 'Room de prueba'}, follow=True)
            room_test = Thread.objects.get(name='Room de prueba')

        self.assertIsInstance(room_test, Thread)
        self.assertEqual(response.status_code, 200)

    def test_room_does_not_exists(self):

        csrf_client = Client(enforce_csrf_checks=False)
        if csrf_client.login(**self.login_credentials):
            csrf_client.post(
                '/rooms/', {'name': 'Room de prueba'}, follow=True)
            detail_response = csrf_client.get('/rooms/2')
        self.assertEqual(detail_response.status_code, 404)

    def test_room_detail_view(self):

        csrf_client = Client(enforce_csrf_checks=False)
        if csrf_client.login(**self.login_credentials):
            response = csrf_client.post(
                '/rooms/', {'name': 'Room de prueba'}, follow=True)
            detail_response = csrf_client.get('/rooms/1')
        self.assertEqual(detail_response.status_code, 200)
        # Asert queryset has 1 object
        self.assertEqual(response.context['object_list'].count(), 1)
