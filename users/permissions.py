from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == request.user:
            return True
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return False
