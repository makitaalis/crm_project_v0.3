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