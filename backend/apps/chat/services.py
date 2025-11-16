from django.db import transaction
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from apps.chat.models import Chat, Message
from apps.users.models import User


class ChatService:
    @staticmethod
    def get_chat_by_id(chat_id):
        return get_object_or_404(Chat, id=chat_id)

    @staticmethod
    def get_user_chats(user):
        return Chat.objects.filter(
            participants=user
        ).prefetch_related('participants').annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time')

    @staticmethod
    def get_chat_between_users(user1, user2):
        chats = Chat.objects.filter(participants=user1).filter(participants=user2)
        for chat in chats:
            if chat.participants.count() == 2:
                return chat
        return None

    @staticmethod
    @transaction.atomic
    def create_chat(user1, user2):
        existing_chat = ChatService.get_chat_between_users(user1, user2)
        if existing_chat:
            return existing_chat, False

        chat = Chat.objects.create()
        chat.participants.add(user1, user2)
        return chat, True

    @staticmethod
    def user_is_participant(chat, user):
        return chat.participants.filter(id=user.id).exists()


class MessageService:
    @staticmethod
    def get_message_by_id(message_id):
        return get_object_or_404(Message, id=message_id)

    @staticmethod
    def get_chat_messages(chat, limit=None):
        queryset = Message.objects.filter(chat=chat).select_related('sender').order_by('created_at')
        if limit:
            queryset = queryset[:limit]
        return queryset

    @staticmethod
    @transaction.atomic
    def create_message(chat, sender, content):
        message = Message.objects.create(
            chat=chat,
            sender=sender,
            content=content
        )
        chat.save()
        return message

    @staticmethod
    @transaction.atomic
    def mark_message_as_read(message):
        if not message.is_read:
            message.is_read = True
            message.save(update_fields=['is_read'])
        return message

    @staticmethod
    @transaction.atomic
    def mark_chat_messages_as_read(chat, user):
        messages_to_update = list(Message.objects.filter(
            chat=chat,
            is_read=False
        ).exclude(sender=user).values_list('id', 'sender_id'))

        updated_count = Message.objects.filter(
            chat=chat,
            is_read=False
        ).exclude(sender=user).update(is_read=True)

        return updated_count, messages_to_update
