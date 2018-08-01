from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('birth_date', 'address', 'photo')


class UserSerializer(ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'user_profile')
    
    def validate(self, data):
        if datetime.now().year - data['user_profile'].get('birth_date').year < 18:
            raise ValidationError('Only 18+ users are able to register!')
        return data
    
    def create(self, data):
        user_profile = data.pop('user_profile')
        user = User.objects.create(**data)
        user.set_password(data.get('password'))
        user.save()
        UserProfile.objects.create(user=user, **user_profile)
        return user


