from django.db import models
from accounts.models import User

NOTIF_TYPES = [
    ('message', 'New Message'),
    ('collab_request', 'Collaboration Request'),
    ('application', 'Campaign Application'),
    ('accepted', 'Offer Accepted'),
    ('rejected', 'Offer Rejected'),
    ('review', 'Review Received'),
    ('system', 'System'),
]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIF_TYPES, default='system')
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"