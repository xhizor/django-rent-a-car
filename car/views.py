from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import Car, Gallery, Model
from .serializers import CarSerializer, GallerySerializer


class CarViewset(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('^name', '^model__name')

    def get_queryset(self):  # Get Car QuerySet - filtering based on QueryString params
        if 'year_from' in self.request.query_params:
            year_from = self.request.query_params.get('year_from')
            year_to = self.request.query_params.get('year_to')
            return self.queryset.filter(available__exact=True)\
                                .filter(model_year__gte=year_from)\
                                .filter(model_year__lte=year_to)

        elif 'price_from' in self.request.query_params:
            price_from = self.request.query_params.get('price_from')
            price_to = self.request.query_params.get('price_to')
            return self.queryset.filter(available__exact=True)\
                                .filter(price_hourly__gte=price_from)\
                                .filter(price_hourly__lte=price_to)

        elif self.request.query_params.get('top_rated'):
            return self.queryset.filter(available__exact=True) \
                                .filter(rate__exact=5)

        elif 'fuel_type' in self.request.query_params:
            fuel_type = self.request.query_params.get('fuel_type')
            return self.queryset.filter(available__exact=True)\
                                .filter(engine__fuel_type__name__exact=fuel_type)
        return self.queryset.filter(available=True)

    @action(methods=['get'], detail=True)
    def gallery(self, request, pk):
        car = self.get_object()
        queryset = Gallery.objects.filter(car=car)
        serializer = GallerySerializer(instance=queryset, many=True)
        return Response(serializer.data)


class ViewCarsAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'car/view_cars.html'

    def get(self, request):
        brands = Model.objects.all()
        return Response({'brands': brands})


class GetCarInfoAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'car/get_car_info.html'

    def get(self, request, pk=None):
        return Response()





