from django.contrib import admin
from .models import Campaign, CampaignApplication, CollaborationRequest

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'budget', 'status', 'deadline', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'brand__company_name']

admin.site.register(CampaignApplication)
admin.site.register(CollaborationRequest)