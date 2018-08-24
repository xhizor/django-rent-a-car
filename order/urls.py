from django.urls import path
from order.views import CreateOrderAPIView, CheckCouponAPIView, admin_send_pdf_order_detail_to_email, \
    GetOrdersAPIView

app_name = 'order'

urlpatterns = [
    path('create/', CreateOrderAPIView.as_view(), name='create'),
    path('check-coupon/', CheckCouponAPIView.as_view(), name='check_coupon'),
    path('admin/order/<int:pk>/send-pdf/', admin_send_pdf_order_detail_to_email, name='send_pdf_to_email'),
    path('get-orders/', GetOrdersAPIView.as_view(), name='get_orders')
]