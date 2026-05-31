from django.contrib import admin
from .models import BrandProfile, Bookmark

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry', 'is_verified', 'total_campaigns']
    list_filter = ['industry', 'is_verified']

admin.site.register(Bookmark)