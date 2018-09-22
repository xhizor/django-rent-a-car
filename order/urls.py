from django.urls import path
from order.views import CreateOrderView, CheckCouponView, admin_send_pdf_order_detail_to_email, \
    GetOrdersView, CancelOrderView, StripePaymentView, RateCarView

app_name = 'order'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    path('check-coupon/', CheckCouponView.as_view(), name='check_coupon'),
    path('admin/order/<int:pk>/send-pdf/', admin_send_pdf_order_detail_to_email, name='send_pdf_to_email'),
    path('get-orders/', GetOrdersView.as_view(), name='get_orders'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
    path('<int:pk>/payment/', StripePaymentView.as_view(), name='payment'),
    path('<int:pk>/rate-car/', RateCarView.as_view(), name='rate_car'),
]



