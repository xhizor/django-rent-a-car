from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class TestLoginAPI(APITestCase):
    def setUp(self):
        user = User(username='test_user', email='test_user@test.com')
        user.set_password('test_pass')
        user.save()

    def test_jwt_valid_user(self):
        data = {'username': 'test_user',
                'password': 'test_pass'}
        url = reverse('account:get_jwt')
        r = self.client.post(url, data=data, format='json')
        self.assertEqual(r.status_code, HTTP_200_OK)
        self.assertTrue(r.data.get('token'))

    def test_jwt_invalid_user(self):
        data = {'username': 'test_user1',
                'password': 'test_pass1'}
        url = reverse('account:get_jwt')
        r = self.client.post(url, data=data, format='json')
        self.assertEqual(r.status_code, HTTP_400_BAD_REQUEST)
        self.assertFalse(r.data.get('token'))

