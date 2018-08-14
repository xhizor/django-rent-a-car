from rest_framework import routers
from .views import CarViewset

app_name = 'car'

router = routers.DefaultRouter()
router.register('cars', CarViewset)

urlpatterns = router.urls
