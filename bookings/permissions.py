from rest_framework.permissions import BasePermission


class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsListingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.listing.owner == request.user
