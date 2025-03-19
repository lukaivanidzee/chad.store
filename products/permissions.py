from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsObjectOwnerReadOnly(BasePermission):
    def has_object_permission(self, requset, view, obj):
        if requset.method is SAFE_METHODS:
            return True
        return requset.user ==obj.user