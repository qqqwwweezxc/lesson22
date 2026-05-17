from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.is_authenticated

        if request.method == "DELETE":
            return request.user.is_staff

        return request.user.is_authenticated