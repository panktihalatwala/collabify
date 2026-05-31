import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        user = self.scope['user']

        if not user.is_authenticated:
            return

        if message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'typing_indicator',
                    'user': user.username,
                    'is_typing': data.get('is_typing', False),
                }
            )
        else:
            content = data.get('message', '').strip()
            if content:
                message, other_user = await self.save_message_and_notify(
                    user, content
                )
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        'type': 'chat_message',
                        'message': content,
                        'sender': user.username,
                        'sender_id': user.pk,
                        'sender_name': await self.get_full_name(user),
                        'message_id': message.pk,
                        'timestamp': message.created_at.strftime('%H:%M'),
                    }
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing'],
        }))

    @database_sync_to_async
    def get_full_name(self, user):
        return user.get_full_name() or user.username

    @database_sync_to_async
    def save_message_and_notify(self, user, content):
        from .models import ChatRoom, Message
        from notifications.models import Notification
        room = ChatRoom.objects.get(pk=self.room_id)
        message = Message.objects.create(
            room=room,
            sender=user,
            content=content
        )
        # Send notification to the other participant
        other_user = room.participants.exclude(pk=user.pk).first()
        if other_user:
            Notification.objects.create(
                user=other_user,
                title=f'New message from {user.get_full_name() or user.username}',
                message=content[:100],
                notification_type='message',
                link=f'/messaging/{room.pk}/'
            )
        return message, other_user