from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class IsStaffRole(permissions.BasePermission):
    """Admin or Staff."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff_role)


class IsOwnerOrStaff(permissions.BasePermission):
    """Object-level: owner (client) can access their own record, staff can access any."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff_role:
            return True
        owner = getattr(obj, "created_by", None) or getattr(obj, "requested_by", None) or getattr(obj, "user", None)
        return owner == request.user
