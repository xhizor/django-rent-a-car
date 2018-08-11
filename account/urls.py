from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import LoginView, CreateUserView, DashboardView, LogoutView, AuthUserView, \
    AuthUserProfileViewSet, UserProfileUpdateView

app_name = 'account'

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='get_jwt'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth-user/', AuthUserView.as_view(), name='auth_user'),
    path('auth-user-profile/', AuthUserProfileViewSet.as_view({'get': 'list'}),
         name='auth_user_profile'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/update/', UserProfileUpdateView.as_view(), name='update')
]