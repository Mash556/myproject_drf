from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwnerOrAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Разрешение для администраторов
        if request.user and request.user.is_staff:
            return True

        # Разрешение для владельцев
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешение для владельцев
        return obj.user == request.user if request.user and request.user.is_authenticated else False