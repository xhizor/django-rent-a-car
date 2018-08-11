from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('birth_date', 'address', 'photo')

    def validate(self, data):
        if datetime.today().year - data.get('birth_date').year < 18:
            raise ValidationError('Only 18+ users are able to register!')
        return data


class UserSerializer(ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'user_profile')

    def create(self, data):
        user_profile = data.pop('user_profile')
        user = User.objects.create(**data)
        user.set_password(data.get('password'))
        user.save()
        UserProfile.objects.create(user=user, **user_profile)
        return user

    def update(self, instance, data):
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.save()
        return instance

