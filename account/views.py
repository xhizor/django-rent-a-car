from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .forms import UserForm
from .serializers import UserSerializer


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
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({'form': UserForm})

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('home')
        return Response({'form': UserForm}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout View for Github Auth User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return redirect('home')







