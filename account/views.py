from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = UserProfile
    serializer_class = UserSerializer
    permission_classes = [AllowAny]





