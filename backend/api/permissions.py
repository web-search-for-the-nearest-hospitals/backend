from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        del view
        return request.user.is_authenticated and request.user.is_admin


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        del view
        return request.method in permissions.SAFE_METHODS


class IsAdminOwnerModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
