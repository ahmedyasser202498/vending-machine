from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSellerOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'seller'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.seller == request.user


class IsBuyerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'buyer'