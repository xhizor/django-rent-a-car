from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
#from .models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        #model = Profile
        fields = ['username', 'email', 'password', 'first_name',
                  'last_name', 'address', 'photo']

    def create(self, data):
        user = User.objects.create(username=data.get('username'),
                                   email=data.get('email'),
                                   first_name=data.get('first_name'),
                                   last_name=data.get('last_name'))
        user.set_password(data.get('password'))
        user_obj = user.save(commit=False)
        #profile = Profile.objects.create(user=user_obj, address=data.get('address'),
         #                                photo=data.get('photo'))
        return user



