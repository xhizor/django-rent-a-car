from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Generic API View for creating a new user.
    """
    model = UserProfile
    serializer_class = UserSerializer
    permission_classes = [AllowAny]





