from django.db import models
from accounts.models import User
from influencers.models import InfluencerProfile
from brands.models import BrandProfile

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.influencer or self.brand
        return f"{self.reviewer.username} → {target} ({self.rating}★)"