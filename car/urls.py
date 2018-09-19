from django.urls import path
from rest_framework import routers
from .views import CarViewSet, GetCarsView, GetCarInfoView

app_name = 'car'

urlpatterns = [
    path('', GetCarsView.as_view(), name='view_cars'),
    path('<int:pk>/info/', GetCarInfoView.as_view(), name='get_car_info'),

]

router = routers.DefaultRouter()
router.register('list', CarViewSet)

urlpatterns += router.urls

