from django.shortcuts import redirect
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
        return Response({'form': UserForm, 'error': True},
                        status=HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    """
    API View for creating a new user (GET, POST)
    Redirect to Login View after successful registration.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/dashboard.html'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response()



