from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, Coupon


@admin.register(Coupon)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'expired')
    list_filter = ('expired',)
    list_editable = ('discount', 'expired')


def approve_order(modeladmin, request, queryset):
    queryset.update(approved=True)
    car = queryset[0].car
    car.available = False
    car.save()
    approve_order.short_description = 'Approve order'


@admin.register(Order)
class ModelAdmin(admin.ModelAdmin):
    def send_pdf_order_detail_to_email(self, order):
        return format_html('<a href="{}" onclick="return confirm(\'Are you sure?\')">Send Email</a>',
                           reverse('order:send_pdf_to_email', kwargs={'pk': order.pk}))

    send_pdf_order_detail_to_email.short_description = 'Send PDF Order detail to email'

    list_display = ('start_date', 'end_date', 'user', 'car', 'approved', 'canceled',
                    'finished', 'paid', 'send_pdf_order_detail_to_email')
    search_fields = ('user__username', 'car__model__name', 'car__name')
    list_filter = ('approved', 'canceled', 'finished')
    list_editable = ('approved', 'canceled', 'finished', 'paid')
    actions = (approve_order,)

