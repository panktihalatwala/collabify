from django.db import models
from brands.models import BrandProfile
from influencers.models import InfluencerProfile

STATUS_CHOICES = [
    ('open', 'Open'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('closed', 'Closed'),
    ('paused', 'Paused'),
]

COLLAB_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('negotiating', 'Negotiating'),
    ('completed', 'Completed'),
]

class Campaign(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=300)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    target_audience = models.TextField(blank=True)
    required_niche = models.CharField(max_length=50, blank=True)
    platforms = models.CharField(max_length=200, blank=True)
    deliverables = models.TextField(blank=True)
    deadline = models.DateField()
    influencer_count = models.PositiveIntegerField(default=1)
    hashtags = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    banner = models.ImageField(upload_to='campaign_banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CampaignApplication(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='applications')
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=COLLAB_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'influencer')

    def __str__(self):
        return f"{self.influencer.user.username} → {self.campaign.title}"

class CollaborationRequest(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name='collab_requests')
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='collab_requests')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=COLLAB_STATUS, default='pending')
    counter_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    counter_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.company_name} → {self.influencer.user.username}"