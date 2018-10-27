from win10toast import ToastNotifier
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.html import format_html
from .models import Order, Coupon
from order.task import send_order_status_to_email


@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'expired')
    list_filter = ('expired',)
    list_editable = ('discount', 'expired')


def approve_order(modeladmin, request, queryset):
    queryset.update(approved=True)
    car = queryset[0].car
    car.available = False
    car.save()
    approve_order.short_description = 'Approve order'


def finish_order(modeladmin, request, queryset):
    order_end_date = parse_datetime(queryset[0].end_date)
    is_paid = queryset[0].paid
    now = timezone.now()
    if is_paid and now >= order_end_date:
        queryset.update(finished=True)
        car = queryset[0].car
        car.available = True
        car.save()
        pk = queryset[0].pk
        send_order_status_to_email.delay(pk, status='finished')
    else:
        toaster = ToastNotifier()
        toaster.show_toast('Error Notification!', "You can't finish this Order yet.", duration=3)
    finish_order.short_description = 'Finish order'


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    def send_pdf_order_detail_to_email(self, order):
        return format_html('<a href="{}" onclick="return confirm(\'Are you sure?\')">Send Email</a>',
                           reverse('order:send_pdf_to_email', kwargs={'pk': order.pk}))

    send_pdf_order_detail_to_email.short_description = 'Send PDF Order detail to email'

    list_display = ('start_date', 'end_date', 'user', 'car', 'approved', 'canceled',
                    'finished', 'paid', 'rate', 'send_pdf_order_detail_to_email')
    search_fields = ('user__username', 'car__model__name', 'car__name')
    list_filter = ('approved', 'canceled', 'finished', 'rate')
    list_editable = ('approved', 'canceled', 'finished', 'paid')
    actions = (approve_order, finish_order)


