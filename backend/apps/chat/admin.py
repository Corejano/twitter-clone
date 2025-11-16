from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['participants']

    def get_participants(self, obj):
        return ', '.join([p.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'sender', 'content_preview', 'created_at', 'is_read']
    list_filter = ['created_at', 'is_read']
    search_fields = ['sender__username', 'content']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['chat', 'sender']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
