from django.db import models
from accounts.models import User

REPORT_TYPES = [
    ('scam', 'Scam Account'),
    ('fake', 'Fake Influencer'),
    ('harassment', 'Harassment'),
    ('inappropriate', 'Inappropriate Content'),
    ('other', 'Other'),
]

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filed_reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_against')
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.username} reported {self.reported_user.username}"