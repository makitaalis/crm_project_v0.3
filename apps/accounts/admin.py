from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LoginHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_blocked', 'last_activity')
    list_filter = ('role', 'is_blocked', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('CRM информация', {
            'fields': ('role', 'is_blocked', 'created_by')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CRM информация', {
            'fields': ('role', 'is_blocked')
        }),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'timestamp', 'success')
    list_filter = ('success', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'timestamp', 'success')