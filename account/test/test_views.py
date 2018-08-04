import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED


@pytest.fixture
def test_user(django_user_model):
    user = django_user_model.objects.create_user(username='test_user',
                                                 email='test@test.com',
                                                 password='test_pass')
    return user


def test_jwt_200(test_user, client):
    url = reverse('account:get_jwt')
    data = {'username': 'test_user',
            'password': 'test_pass'}
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_200_OK
    assert r.data.get('token')


def test_jwt_400(test_user, client):
    url = reverse('account:get_jwt')
    data = {'username': 'test_user1',
            'password': 'test_pass1'}
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert not r.data.get('token')


@pytest.mark.django_db
def test_register_201(client):
    url = reverse('account:register')
    data = {'username': 'test_user',
            'email': 'test_email@email.com',
            'password': 'test_pass',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '1993-05-05',
            }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_201_CREATED
    json_response_username = r.json().get('username')
    assert json_response_username == 'test_user'


@pytest.mark.django_db
def test_register_400(client):
    url = reverse('account:register')
    data = {'username': 'test_user',
            'email': 'email.com',  # Invalid email address
            'password': 'test_pass',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '1993-05-05',
            }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_birth_date_field_validation_error(client):
    url = reverse('account:register')
    data = {'username': 'test_user1',
            'email': 'test_email@ema il.com',
            'password': 'test_pass',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'user_profile.address': 'test_address',
            'user_profile.birth_date': '2005-05-05',
    }
    r = client.post(url, data=data, format='json')
    assert r.status_code == HTTP_400_BAD_REQUEST
    json_response_errors = r.json().get('user_profile')\
                                   .get('non_field_errors')
    assert json_response_errors


#@pytest.mark.django_db
#def test_home_200(test_user, client):
    #url = reverse('home')
    #payload = api_settings.JWT_PAYLOAD_HANDLER(test_user)
    #token = api_settings.JWT_ENCODE_HANDLER(payload)
    #client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    #client.force_authenticate(user=test_user, token=token)
    #r = client.get(url)
    #assert r

def test_home_200(test_user, client):
    url = reverse('home')
    r = client.get(url)
    assert r.status_code == 200
