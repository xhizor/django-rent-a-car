from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserSerializer


class HomeView(APIView):
    """
    Home Page Template API View (GET).
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'base.html'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response()


class LoginView(APIView):
    """
    Login Page Template API View (GET, POST).
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/login.html'
    permission_classes = [AllowAny]

    def get(self, request):
        return Response()


class CreateUserView(CreateAPIView):
    """
    API View for creating a new user (POST).
    Return user instance with 201 CREATED status code.
    """
    model = UserProfile
    serializer_class = UserSerializer
    permission_classes = [AllowAny]