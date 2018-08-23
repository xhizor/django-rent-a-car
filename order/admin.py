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
    queryset.update(approval=True)
    approve_order.short_description = 'Approve order'


@admin.register(Order)
class ModelAdmin(admin.ModelAdmin):
    def order_detail_to_pdf(self, obj):
        return format_html('<a href="{}">Send PDF to email</a>',
                           reverse('order:order_detail_to_pdf', kwargs={'pk': obj.pk}))

    order_detail_to_pdf.short_description = 'Send PDF Order detail to email'

    list_display = ('start_date', 'end_date', 'user', 'car', 'approval', 'finished', 'order_detail_to_pdf')
    search_fields = ('user__username', 'car__model__name', 'car__name')
    list_filter = ('approval', 'finished')
    actions = (approve_order,)

