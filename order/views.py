from io import BytesIO
from json import loads
from weasyprint import HTML
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import format_html
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car, Coupon, Order
from .serializers import OrderSerializer


class CheckCouponAPIView(APIView):
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


class CreateOrderAPIView(CreateAPIView):
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


class GetOrdersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('active') == 'True':
            return self.queryset.filter(approval=True, finished=False, user=self.request.user)
        if self.request.query_params.get('finished') == 'True':
            return self.queryset.filter(approval=True, finished=True, user=self.request.user)
        return self.queryset.filter(approval=False, user=self.request.user)


@staff_member_required
def admin_send_pdf_order_detail_to_email(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.approval:
        html = render_to_string('order/order_detail_pdf.html', {'order': order})
        out = BytesIO()
        HTML(string=html).write_pdf(out)
        subject = 'Rent-a-car Order detail'
        message = f'We approved your Order #{order.pk}. You can see Order detail in PDF attachment. '\
                  'Thank you for using our Rent-a-car service!'
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
        email.attach('Order#{}_{}.pdf'.format(order.pk, order.car.name),
                     out.getvalue(), 'application/pdf')
        email.send()
        return HttpResponse(f'Email has been sent successfully to: {request.user.get_full_name()}!')
    return HttpResponseBadRequest('Oops! This order is not approved yet.')


