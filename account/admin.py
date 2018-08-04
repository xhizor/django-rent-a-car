from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'full_name', 'birth_date', 'address', 'date_joined')
    list_editable = ('address',)
    search_fields = ('user__username', 'user__email', 'address',)
    ordering = ('user__date_joined',)

    def email(self, obj):
        return obj.user.email

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def date_joined(self, obj):
        return obj.user.date_joined




