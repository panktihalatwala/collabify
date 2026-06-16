from django.db import models
from accounts.models import User
from campaigns.models import CollaborationRequest

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('released', 'Released'),
    ('completed', 'Completed'),
    ('disputed', 'Disputed'),
]

class Transaction(models.Model):
    collaboration = models.OneToOneField(
        CollaborationRequest,
        on_delete=models.CASCADE,
        related_name='transaction'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_payments'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='received_payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_id} — ₹{self.amount}"