from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from apps.chat.models import Chat, Message
from apps.chat.serializers import (
    ChatSerializer,
    ChatDetailSerializer,
    ChatCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from apps.chat.services import ChatService, MessageService
from apps.chat.permissions import IsParticipant
from apps.users.models import User


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatService.get_user_chats(self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChatDetailSerializer
        elif self.action == 'create':
            return ChatCreateSerializer
        return ChatSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'messages', 'send_message', 'mark_as_read']:
            return [IsAuthenticated(), IsParticipant()]
        return [IsAuthenticated()]

    @method_decorator(ratelimit(key='user', rate='30/m', method='POST'))
    def create(self, request, *args, **kwargs):
        serializer = ChatCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        participant_id = serializer.validated_data['participant_id']
        try:
            other_user = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        chat, created = ChatService.create_chat(request.user, other_user)

        response_serializer = ChatSerializer(chat, context={'request': request})
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        chat = self.get_object()
        self.check_object_permissions(request, chat)
        serializer = ChatDetailSerializer(chat, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        self.check_object_permissions(request, chat)

        messages = MessageService.get_chat_messages(chat)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(ratelimit(key='user', rate='60/m', method='POST'))
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat = self.get_object()
        self.check_object_permissions(request, chat)

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = MessageService.create_message(
            chat=chat,
            sender=request.user,
            content=serializer.validated_data['content']
        )

        response_serializer = MessageSerializer(message, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        chat = self.get_object()
        self.check_object_permissions(request, chat)

        updated_count = MessageService.mark_chat_messages_as_read(chat, request.user)
        return Response(
            {'message': f'{updated_count} messages marked as read.'},
            status=status.HTTP_200_OK
        )


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        user_chats = Chat.objects.filter(participants=self.request.user)
        return Message.objects.filter(chat__in=user_chats).select_related('sender', 'chat')

    @method_decorator(ratelimit(key='user', rate='60/m', method='PATCH'))
    @action(detail=True, methods=['patch'], url_path='read')
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        self.check_object_permissions(request, message)

        if message.sender == request.user:
            return Response(
                {'error': 'Cannot mark own message as read.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        MessageService.mark_message_as_read(message)
        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data)
