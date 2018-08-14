from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import Car, Gallery
from .serializers import CarSerializer, GallerySerializer


class CarViewset(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly)
    serializer_class = CarSerializer
    queryset = Car.objects.filter(available=True)

    @action(methods=['get'], detail=True, 
            permission_classes=[IsAuthenticatedOrReadOnly])
    def gallery(self, request, pk):
        car = self.get_object()
        queryset = Gallery.objects.filter(car=car)
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)
        





