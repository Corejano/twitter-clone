import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError
from apps.chat.models import Chat, Message
from apps.chat.services import ChatService, MessageService


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        chat = await self.get_chat()
        if not chat:
            await self.close()
            return

        is_participant = await self.check_user_is_participant(chat)
        if not is_participant:
            await self.close()
            return

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
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message':
                content = data.get('content', '').strip()

                if not content:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Message content cannot be empty.'
                    }))
                    return

                chat = await self.get_chat()
                message = await self.create_message(chat, content)

                message_data = await self.serialize_message(message)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_data
                    }
                )

            elif message_type == 'typing':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'user_id': str(self.user.id),
                        'username': self.user.username,
                        'is_typing': data.get('is_typing', False)
                    }
                )

            elif message_type == 'mark_read':
                message_id = data.get('message_id')
                if message_id:
                    await self.mark_message_read(message_id)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))

    async def typing_indicator(self, event):
        if str(self.user.id) != event['user_id']:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user_id': event['user_id'],
                'username': event['username'],
                'is_typing': event['is_typing']
            }))

    @database_sync_to_async
    def get_chat(self):
        try:
            return Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def check_user_is_participant(self, chat):
        return chat.participants.filter(id=self.user.id).exists()

    @database_sync_to_async
    def create_message(self, chat, content):
        return MessageService.create_message(
            chat=chat,
            sender=self.user,
            content=content
        )

    @database_sync_to_async
    def serialize_message(self, message):
        return {
            'id': str(message.id),
            'chat_id': str(message.chat.id),
            'sender': {
                'id': str(message.sender.id),
                'username': message.sender.username,
                'full_name': message.sender.full_name,
                'avatar': message.sender.avatar.url if message.sender.avatar else None,
            },
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'is_read': message.is_read
        }

    @database_sync_to_async
    def mark_message_read(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            if message.sender != self.user and not message.is_read:
                MessageService.mark_message_as_read(message)
        except Message.DoesNotExist:
            pass
