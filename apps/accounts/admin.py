# apps/accounts/admin.py
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


# apps/clients/admin.py
from django.contrib import admin
from .models import Client, ClientHistory


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'source', 'created_at', 'created_by')
    list_filter = ('source', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at', 'created_by')


@admin.register(ClientHistory)
class ClientHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'field_name', 'user', 'timestamp')
    list_filter = ('field_name', 'timestamp')
    readonly_fields = ('client', 'user', 'field_name', 'old_value', 'new_value', 'timestamp')


# apps/applications/admin.py
from django.contrib import admin
from .models import Application, Status, Category, ApplicationHistory, ApplicationComment


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color', 'is_final', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'operator', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'operator', 'created_at')
    search_fields = ('client__name', 'client__phone', 'notes')
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at', 'created_by')


@admin.register(ApplicationHistory)
class ApplicationHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    readonly_fields = ('application', 'user', 'action', 'comment', 'timestamp')


@admin.register(ApplicationComment)
class ApplicationCommentAdmin(admin.ModelAdmin):
    list_display = ('application', 'user', 'timestamp')
    list_filter = ('timestamp',)
    readonly_fields = ('application', 'user', 'text', 'timestamp')