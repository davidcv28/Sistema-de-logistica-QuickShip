from rest_framework import permissions

####USER ANONIMOUS PERMISSION

"""
<----Permiso para usuario anonimos---->

"""
class UserAnonimousPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True