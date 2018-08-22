from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Car
from .serializers import OrderSerializer


class CreateOrderAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        pk = self.request.data.get('pk')
        car = Car.objects.get(pk=pk)
        serializer.save(user=self.request.user, car=car)


