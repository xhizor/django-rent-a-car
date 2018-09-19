from json import loads
import stripe
from decouple import config
from win10toast import ToastNotifier
from django.db.models import Q
from django.utils import timezone
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.html import format_html
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .task import send_pdf_to_email, send_order_status_to_email
from .models import Car, Coupon, Order
from .serializers import OrderSerializer


class CheckCouponView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = loads(request.body.decode('utf-8')).get('code')
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon:
                coupon_expired_date = Coupon.objects.get(code=code).expired
                now = timezone.now()
                if now > coupon_expired_date:
                    return Response({'status': 'expired'})
                return Response({'status': 'valid', 'discount': coupon.discount})
        except Coupon.DoesNotExist:
            return Response({'status': 'invalid'})


class CreateOrderView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        pk = self.request.data.get('pk')
        car = Car.objects.get(pk=pk)
        serializer.save(user=self.request.user, car=car)
        messages.info(self.request,
                      format_html('New order from {}! <br> Click <a href="{}"> here </a> to view order.',
                                  self.request.user.get_full_name(), 'http://localhost:8000/admin/order/order/' +
                                  str(serializer.data.get('id')) + '/change/'))
        toaster = ToastNotifier()
        toaster.show_toast('New Order Notification!', f'You ordered a new car', duration=3)


class GetOrdersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('active') == 'True':
            return self.queryset\
                   .filter(Q(approved=True, canceled=False, finished=False, paid=False) |
                           Q(approved=True, canceled=False, finished=False, paid=True))
        if self.request.query_params.get('canceled') == 'True':
            return self.queryset\
                   .filter(canceled=True, approved=False, finished=False, paid=False)
        if self.request.query_params.get('finished') == 'True':
            return self.queryset\
                .filter(approved=True, paid=True, finished=True, canceled=False)
        return self.queryset\
            .filter(approved=False, canceled=False, finished=False, paid=False, user=self.request.user)


class CancelOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.canceled = True
        order.save()
        send_order_status_to_email(pk, status='canceled')
        messages.info(self.request,
                      format_html('{} cancel the Order <a href="{}">{}</a>',
                                  self.request.user.get_full_name(),
                                  f'http://localhost:8000/admin/order/order/{order.pk}',
                                  f'#{order.pk}'))
        return Response({'canceled': True})


class StripePaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    stripe.api_key = config('STRIPE_SECRET_KEY')

    def post(self, request, pk):
        try:
            stripe_id = loads(request.body.decode('utf-8')).get('stripe_id')
            total_price = loads(request.body.decode('utf-8')).get('total_price')
            stripe.Charge.create(amount=int(total_price), currency='USD',
                                 description='Payment from Rent-a-car web site', card=stripe_id)
            order = Order.objects.get(pk=pk)
            order.paid = True
            order.save()
            messages.info(self.request,
                          format_html('{} paid the Order <a href="{}">{}</a>',
                                      order.user.get_full_name(),
                                      f'http://localhost:8000/admin/order/order/{order.pk}',
                                      f'#{order.pk}'))
            send_order_status_to_email.delay(pk, status='paid')
            return Response()
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)


@staff_member_required
def admin_send_pdf_order_detail_to_email(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.approved and not order.paid:
        send_pdf_to_email.delay(pk)
        return HttpResponse(f'<i>Email has been sent successfully to {order.user.get_full_name()}!</i>')
    return HttpResponseBadRequest('<i>Oops! The order is not approved yet or it has already been paid.</i>')


