from rest_framework.serializers import ModelSerializer
from .models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 2
