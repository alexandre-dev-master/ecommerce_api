from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to edit or create objects.
    Anyone can perform safe actions (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        # Allow any visitor to read the data (GET requests)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is authenticated AND has staff/admin privileges
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)