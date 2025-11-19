from rest_framework import serializers
from apps.chat.models import Chat, Message
from apps.users.serializers import UserListSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserListSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'created_at', 'is_read']
        read_only_fields = ['id', 'chat', 'sender', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Message content cannot be empty.')
        return value.strip()


class ChatSerializer(serializers.ModelSerializer):
    participants = UserListSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message', 'unread_count', 'other_participant']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.get_last_message()
        if last_message:
            return {
                'id': str(last_message.id),
                'content': last_message.content,
                'sender_id': str(last_message.sender.id),
                'sender_username': last_message.sender.username,
                'created_at': last_message.created_at,
                'is_read': last_message.is_read
            }
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.get_unread_count(request.user)
        return 0

    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.get_other_participant(request.user)
            if other:
                return UserListSerializer(other, context=self.context).data
        return None


class ChatDetailSerializer(serializers.ModelSerializer):
    participants = UserListSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at', 'other_participant']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.get_other_participant(request.user)
            if other:
                return UserListSerializer(other, context=self.context).data
        return None


class ChatCreateSerializer(serializers.Serializer):
    participant_id = serializers.UUIDField()

    def validate_participant_id(self, value):
        from apps.users.models import User

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if str(request.user.id) == str(value):
                raise serializers.ValidationError('You cannot create a chat with yourself.')

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError('User not found.')

        return value
