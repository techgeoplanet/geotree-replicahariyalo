# permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow write permissions to admin users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class IsPatnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow write permissions to admin users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_active

class IsAdminWriteOrAuthenticatedRead(permissions.BasePermission):
    """
    Custom permission to allow write access only to admin users,
    and read access to all authenticated users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff

class IsPartnerWriteOrAuthenticatedRead(permissions.BasePermission):
    """
    Custom permission to allow write access to partners,
    and read access to all authenticated users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to partners
        return request.user and request.user.is_active