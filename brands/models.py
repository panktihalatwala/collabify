from django.db import models
from accounts.models import User
from influencers.models import InfluencerProfile

INDUSTRY_CHOICES = [
    ('fashion', 'Fashion'), ('beauty', 'Beauty & Cosmetics'),
    ('tech', 'Technology'), ('food', 'Food & Beverage'),
    ('health', 'Health & Wellness'), ('finance', 'Finance'),
    ('travel', 'Travel & Hospitality'), ('education', 'Education'),
    ('retail', 'Retail & E-commerce'), ('entertainment', 'Entertainment'),
    ('sports', 'Sports & Fitness'), ('other', 'Other'),
]

class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='other')
    website = models.URLField(blank=True)
    company_size = models.CharField(max_length=50, blank=True, choices=[
        ('1-10', '1-10'), ('11-50', '11-50'), ('51-200', '51-200'),
        ('201-500', '201-500'), ('500+', '500+')
    ])
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='brand_covers/', blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_campaigns = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class Bookmark(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name='bookmarks')
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('brand', 'influencer')

    def __str__(self):
        return f"{self.brand.company_name} bookmarked {self.influencer.user.username}"