from json import loads
from django.utils import timezone
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car, Coupon
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




