import pytest
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_302_FOUND
from rest_framework.test import APIClient
from ..models import UserProfile

# Test credentials
username = 'test_user'
password = 'test_pass'


def test_valid_jwt(django_user_model, client):
    django_user_model.objects.create_user(username=username,
                                          password=password)
    url = reverse('account:get_jwt')
    data = {'username': username,
            'password': password}
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_200_OK
    assert r.data.get('token')


def test_invalid_jwt(django_user_model, client):
    django_user_model.objects.create_user(username=username,
                                          password=password)
    url = reverse('account:get_jwt')
    data = {'username': username + '1',  # Invalid username
            'password': password}
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert not r.data.get('token')


def test_register_get(client):
    url = reverse('account:register')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK
    assert 'csrfmiddlewaretoken' in str(r.content)
    assert 'user_profile.photo' in str(r.content)


@pytest.mark.django_db
def test_valid_register(client):
    url = reverse('account:register')
    data = {'username': username,
            'password': password,
            'email': 'test_email@email.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '1993-05-05',
            }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_302_FOUND


@pytest.mark.django_db
def test_invalid_register(client):
    url = reverse('account:register')
    data = {'username': username,
            'password': password,
            'email': 'email@com',  # Invalid email format
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '1993-05-05',
            }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_birth_date_validation_error(client):
    url = reverse('account:register')
    data = {'username': username,
            'password': password,
            'email': 'test_email@email.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '2015-05-05',
    }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_logout(django_user_model, client):
    django_user_model.objects.create_user(username=username,
                                          password=password)
    client.login(username=username, password=password)

    url = reverse('account:logout')
    r = client.get(url)
    client.logout()
    assert r.status_code == HTTP_302_FOUND


def test_home_get(client):
    url = reverse('home')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK


def test_dashboard(client):
    url = reverse('account:dashboard')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK


def test_auth_user(django_user_model):
    user = django_user_model.objects.create_user(username=username,
                                                 password=password)
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('account:auth_user')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK
    assert r.json().get('username') == 'test_user'


def test_auth_user_profile(django_user_model):
    user = django_user_model.objects.create_user(username=username,
                                                 password=password)
    UserProfile.objects.create(user=user, birth_date='1995-05-05')
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('account:auth_user_profile')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK
    assert r.json()[0].get('birth_date') == '1995-05-05'


