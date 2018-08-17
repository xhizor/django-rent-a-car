from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import Car, Gallery
from .serializers import CarSerializer, GallerySerializer


class CarViewset(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CarSerializer
    queryset = Car.objects.filter(available=True)

    @action(methods=['get'], detail=True)
    def gallery(self, request, pk):
        car = self.get_object()
        queryset = Gallery.objects.filter(car=car)
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)


class ViewCarsAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'car/view_cars.html'

    def get(self, request):
        return Response()


class GetCarInfoAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'car/get_car_info.html'

    def get(self, request, pk=None):
        return Response()




