from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Доступ только для владельца
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "author"):
            return request.user == obj.author
        return False
