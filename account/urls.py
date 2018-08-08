from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import LoginView, CreateUserView, DashboardView

app_name = 'account'

urlpatterns = [
    path('auth/token/', obtain_jwt_token, name='get_jwt'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')

]