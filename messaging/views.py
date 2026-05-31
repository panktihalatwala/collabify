from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ChatRoom, Message
from accounts.models import User

@login_required
def inbox(request):
    rooms = request.user.chat_rooms.prefetch_related(
        'participants', 'messages'
    ).order_by('-created_at')
    room_data = []
    for room in rooms:
        other = room.get_other_user(request.user)
        last_msg = room.messages.last()
        unread = room.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
        room_data.append({
            'room': room,
            'other': other,
            'last_msg': last_msg,
            'unread': unread
        })
    return render(request, 'messaging/inbox.html', {'room_data': room_data})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id)
    if request.user not in room.participants.all():
        return redirect('messaging:inbox')
    messages_qs = room.messages.select_related('sender').all()
    messages_qs.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    other = room.get_other_user(request.user)
    return render(request, 'messaging/chat.html', {
        'room': room,
        'messages': messages_qs,
        'other': other,
    })

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    # Find existing room between these two users
    existing = ChatRoom.objects.filter(
        participants=request.user
    ).filter(participants=other_user)
    if existing.exists():
        return redirect('messaging:chat', room_id=existing.first().pk)
    room = ChatRoom.objects.create()
    room.participants.add(request.user, other_user)
    return redirect('messaging:chat', room_id=room.pk)

@login_required
def select_campaign_to_message(request):
    """Influencer selects which campaign's brand to message"""
    from campaigns.models import CampaignApplication, Campaign
    if request.user.is_influencer_user:
        # Show campaigns the influencer applied to
        applications = CampaignApplication.objects.filter(
            influencer__user=request.user
        ).select_related('campaign__brand__user').order_by('-created_at')
        return render(request, 'messaging/select_campaign.html', {
            'applications': applications,
            'mode': 'influencer'
        })
    else:
        # Brand sees their campaigns with applicants
        from campaigns.models import Campaign
        campaigns = Campaign.objects.filter(
            brand__user=request.user
        ).prefetch_related('applications__influencer__user').order_by('-created_at')
        return render(request, 'messaging/select_campaign.html', {
            'campaigns': campaigns,
            'mode': 'brand'
        })
    
@login_required
def send_message_http(request, room_id):
    """HTTP fallback for when WebSocket is unavailable"""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, pk=room_id)
        if request.user not in room.participants.all():
            from django.http import JsonResponse
            return JsonResponse({'error': 'Not authorized'}, status=403)
        
        content = request.POST.get('message', '').strip()
        if content:
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
            # Send notification to other user
            other_user = room.get_other_user(request.user)
            if other_user:
                from notifications.models import Notification
                Notification.objects.create(
                    user=other_user,
                    title=f'New message from {request.user.get_full_name() or request.user.username}',
                    message=content[:100],
                    notification_type='message',
                    link=f'/messaging/{room.pk}/'
                )
            from django.http import JsonResponse
            return JsonResponse({
                'status': 'ok',
                'message_id': message.pk,
                'content': message.content,
                'timestamp': message.created_at.strftime('%H:%M'),
                'sender_id': request.user.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
            })
    from django.http import JsonResponse
    return JsonResponse({'error': 'Invalid request'}, status=400)