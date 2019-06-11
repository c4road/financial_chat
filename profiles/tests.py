from django.test import TestCase

from .models import User
# Create your tests here.


class TestingModels(TestCase):

    def setUp(self):

        self.credentials = {
            'username': 'testUser1',
            'email': 'testUser1@gmail.com',
            'password': 'testpass'
        }

    def test_create_user(self):

        user = User.objects.create_user(**self.credentials)

        user_test = User.objects.get(username='testUser1')

        self.assertEqual(user, user_test)

    def test_create_super_user(self):

        user = User.objects.create_superuser(**self.credentials)

        self.assertTrue(user.is_staff)


class TestingViews(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'secret'}

        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post(
            '/login/', {'email': 'testuser@email.com', 'password': 'secret'})

        self.assertTrue(response.status_code, 200)

    def test_register(self):

        response = self.client.post(
            '/register/', {
                'username': 'user1',
                            'email': 'user1@gmail.com',
                            'password1': 'secret',
                            'password2': 'secret'
            }, follow=True)

        new_user = User.objects.get(username='user1')
        redirect_chain = response.redirect_chain
        self.assertEqual(response.status_code, 200)
        self.assertEqual(redirect_chain[0][1], 302)
        self.assertTrue(new_user)
