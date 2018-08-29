from decouple import config
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from .models import UserProfile
from .forms import UserForm
from .serializers import UserSerializer, UserProfileSerializer


class HomeView(APIView):
    """
    Home Page Template API View (GET).
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/home.html'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response()


class LoginView(APIView):
    """
    Login Page Template API View (GET).
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/login.html'
    permission_classes = [AllowAny]

    def get(self, request):
        return Response()


class CreateUserView(APIView):
    """
    API View for creating a new user (GET, POST)
    Redirect to Login View after successful registration.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/register.html'
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'form': UserForm})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('account:login')
        return Response({'form': UserForm}, status=HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    """
    User Dashboard Page Template API View (GET).
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/dashboard.html'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response({'form': UserForm,
                         'pub_key': config('STRIPE_PUB_KEY'),
                         'months': range(1, 13),
                         'years': range(2018, 2026)})


class UserProfileUpdateView(APIView):
    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_200_OK)
        return Response({'form': UserForm}, status=HTTP_400_BAD_REQUEST)


class AuthUserView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AuthUserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset


class LogoutView(APIView):
    """
    Logout View for Github Auth User.
    """

    def get(self, request):
        logout(request)
        return redirect('home')







