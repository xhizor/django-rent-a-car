from django.urls import path
from rest_framework import routers
from .views import CarViewset, ViewCarsAPIView, GetCarInfoAPIView

app_name = 'car'

urlpatterns = [
    path('', ViewCarsAPIView.as_view(), name='view_cars'),
    path('<int:pk>/info/', GetCarInfoAPIView.as_view(), name='get_car_info'),

]

router = routers.DefaultRouter()
router.register('list', CarViewset)

urlpatterns += router.urls

