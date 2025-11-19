from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=request.user.id).exists()
        elif hasattr(obj, 'chat'):
            return obj.chat.participants.filter(id=request.user.id).exists()
        return False
