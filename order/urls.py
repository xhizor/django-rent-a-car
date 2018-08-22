from django.urls import path
from order.views import CreateOrderAPIView

app_name = 'order'

urlpatterns = [
    path('create/', CreateOrderAPIView.as_view(), name='create'),
]