from django.contrib import admin
from .models import InfluencerProfile, PortfolioItem

@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'niche', 'followers_count', 'avg_rating', 'total_collaborations']
    list_filter = ['niche']
    search_fields = ['user__username', 'user__email']

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['influencer', 'title', 'media_type', 'created_at']