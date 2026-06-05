from django.db import models
from accounts.models import User

NICHE_CHOICES = [
    ('fashion', 'Fashion'),
    ('beauty', 'Beauty'),
    ('fitness', 'Fitness'),
    ('food', 'Food & Cooking'),
    ('travel', 'Travel'),
    ('tech', 'Tech'),
    ('gaming', 'Gaming'),
    ('lifestyle', 'Lifestyle'),
    ('business', 'Business'),
    ('education', 'Education'),
    ('entertainment', 'Entertainment'),
    ('health', 'Health & Wellness'),
    ('parenting', 'Parenting'),
    ('finance', 'Finance'),
    ('other', 'Other'),
]

PLATFORM_CHOICES = [
    ('instagram', 'Instagram'),
    ('youtube', 'YouTube'),
    
    ('twitter', 'X (Twitter)'),
    ('linkedin', 'LinkedIn'),
    ('facebook', 'Facebook'),
]

class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    niche = models.CharField(max_length=50, choices=NICHE_CHOICES, default='lifestyle')
    followers_count = models.PositiveIntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    collab_price_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    collab_price_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    languages = models.CharField(max_length=200, blank=True, default='Hindi, English')
    cover_image = models.ImageField(upload_to='influencer_covers/', blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    total_collaborations = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.niche}"

class PortfolioItem(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link')
    ]
    influencer = models.ForeignKey(
        InfluencerProfile,
        on_delete=models.CASCADE,
        related_name='portfolio'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    link_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.influencer.user.username} - {self.title}"