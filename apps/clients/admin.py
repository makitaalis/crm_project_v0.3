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

