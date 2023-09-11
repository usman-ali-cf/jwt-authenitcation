from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions
from .models import AuthUser
from django.core.exceptions import ObjectDoesNotExist


class AdminAccess(BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = request.user.id
            user = AuthUser.objects.get(id=user_id)
            if user.role.id == 1:
                return True
            return False
        except ObjectDoesNotExist as e:
            return False


class EditPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            user_id = request.user.id
            user = AuthUser.objects.get(id=user_id)
            if user.role.id == 1:
                return True
            return obj == request.user
        except ObjectDoesNotExist as e:
            return False
