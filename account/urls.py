from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import CreateUserView

app_name = 'account'

urlpatterns = [
    path('api/auth/token/', obtain_jwt_token, name='get_jwt'),
    path('api/register/', CreateUserView.as_view(), name='create_user')
]