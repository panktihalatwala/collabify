from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid
from .models import Transaction
from campaigns.models import CollaborationRequest
from notifications.models import Notification

@login_required
def payment_overview(request, collab_pk):
    collab = get_object_or_404(CollaborationRequest, pk=collab_pk)
    if request.user != collab.brand.user and request.user != collab.influencer.user:
        messages.error(request, 'Not authorized.')
        return redirect('dashboard:home')
    try:
        transaction = collab.transaction
    except:
        transaction = None
    return render(request, 'payments/overview.html', {
        'collab': collab,
        'transaction': transaction,
    })

@login_required
def release_payment(request, collab_pk):
    collab = get_object_or_404(CollaborationRequest, pk=collab_pk)
    if request.user != collab.brand.user:
        messages.error(request, 'Only brands can release payments.')
        return redirect('dashboard:home')
    if collab.status != 'accepted':
        messages.error(request, 'Collaboration must be accepted first.')
        return redirect('payments:overview', collab_pk=collab_pk)
    if request.method == 'POST':
        try:
            existing = collab.transaction
            messages.warning(request, 'Payment already released.')
            return redirect('payments:overview', collab_pk=collab_pk)
        except:
            pass
        # Create transaction
        transaction_id = f"CLB{uuid.uuid4().hex[:10].upper()}"
        transaction = Transaction.objects.create(
            collaboration=collab,
            sender=collab.brand.user,
            receiver=collab.influencer.user,
            amount=collab.payment_amount,
            status='released',
            transaction_id=transaction_id,
            released_at=timezone.now(),
        )
        # Update influencer earnings
        profile = collab.influencer
        profile.total_earnings += collab.payment_amount
        profile.total_collaborations += 1
        profile.save()
        # Update collab status
        collab.status = 'completed'
        collab.save()
        # Notify influencer
        Notification.objects.create(
            user=collab.influencer.user,
            title='Payment Released! 💰',
            message=f'{collab.brand.company_name} released ₹{collab.payment_amount} for your collaboration.',
            notification_type='accepted',
            link=f'/payments/{collab.pk}/'
        )
        messages.success(request, f'Payment of ₹{collab.payment_amount} released successfully!')
        return redirect('payments:overview', collab_pk=collab_pk)
    return render(request, 'payments/confirm_release.html', {
        'collab': collab,
    })

@login_required
def transaction_history(request):
    user = request.user
    if user.role == 'brand':
        transactions = Transaction.objects.filter(
            sender=user
        ).select_related('collaboration', 'receiver').order_by('-created_at')
    else:
        transactions = Transaction.objects.filter(
            receiver=user
        ).select_related('collaboration', 'sender').order_by('-created_at')
    total = sum(t.amount for t in transactions)
    return render(request, 'payments/history.html', {
        'transactions': transactions,
        'total': total,
    })