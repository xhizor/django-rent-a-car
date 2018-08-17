from django.urls import reverse
from rest_framework.status import HTTP_200_OK


def test_view_cars_get(client):
    url = reverse('car:view_cars')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK


def test_get_car_info_get(client):
    url = reverse('car:get_car_info', kwargs={'pk': 1})
    r = client.get(url)
    assert r.status_code == HTTP_200_OK

