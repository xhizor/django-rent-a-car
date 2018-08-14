from rest_framework.serializers import ModelSerializer
from .models import Car, Gallery


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        depth = 1


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


