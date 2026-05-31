from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'reported_user', 'report_type', 'is_resolved', 'created_at']
    list_filter = ['report_type', 'is_resolved']
    search_fields = ['reporter__username', 'reported_user__username']
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_resolved.short_description = 'Mark selected reports as resolved'