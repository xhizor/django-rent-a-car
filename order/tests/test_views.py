import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from car.models import Car

username = 'test_user'
password = 'test_pass'


@pytest.fixture
def test_user(django_user_model):
    return django_user_model.objects.create_user(username=username,
                                                 password=password)


def test_create_valid_order(test_user):
    car = Car.objects.create(name='test_car', model_year='2014',
                             price_hourly=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'end_date': '2018-09-09',
            'total_price': 100,
            'pk': car.pk
           }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_201_CREATED


def test_create_invalid_order(test_user):
    car = Car.objects.create(name='test_car', model_year='2014',
                             price_hourly=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'total_price': 100,
            'pk': car.pk
           }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_400_BAD_REQUEST


def test_create_order_unauthorized(test_user, client):
    car = Car.objects.create(name='test_car', model_year='2014',
                             price_hourly=10)
    client = APIClient()
    data = {'end_date': '2018-09-09',
            'total_price': 100,
            'pk': car.pk
            }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_401_UNAUTHORIZED

