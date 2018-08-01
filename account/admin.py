from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'full_name', 'birth_date', 'address', 'date_joined')
    list_editable = ('address',)

    def email(self, obj):
        return obj.user.email

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def date_joined(self, obj):
        return obj.user.date_joined




