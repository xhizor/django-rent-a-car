from django.urls import path
from order.views import CreateOrderAPIView, CheckCouponAPIView

app_name = 'order'

urlpatterns = [
    path('create/', CreateOrderAPIView.as_view(), name='create'),
    path('check-coupon/', CheckCouponAPIView.as_view(), name='check_coupon'),
]