from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('influencer', 'Influencer'),
        ('brand', 'Brand'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influencer')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Methods — use in views: user.is_influencer()
    def is_influencer(self):
        return self.role == 'influencer'

    def is_brand(self):
        return self.role == 'brand'

    # Properties — use in templates: {{ user.is_influencer_user }}
    @property
    def is_influencer_user(self):
        return self.role == 'influencer'

    @property
    def is_brand_user(self):
        return self.role == 'brand'

    def __str__(self):
        return f"{self.username} ({self.role})"