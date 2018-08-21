from django.contrib import admin
from .models import Order, Coupon


@admin.register(Coupon)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'expired')
    list_filter = ('expired',)
    list_editable = ('discount',)


@admin.register(Order)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'user', 'car', 'coupon', 'approval', 'finished')
    search_fields = ('user__username', 'car__model__name', 'car__name')
    list_filter = ('approval', 'finished')