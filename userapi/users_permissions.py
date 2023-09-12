from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions
from .models import AuthUser, Role
from django.core.exceptions import ObjectDoesNotExist


class SuperAdmin:

    def has_permission(self, request, view):
        try:
            user_id = request.user.id
            user = AuthUser.objects.get(id=user_id)
            role_id = user.role.id
            role = Role.objects.get(id=role_id)
            return role.user_role == "super"
        except ObjectDoesNotExist as e:
            return False


class AdminAccess(BasePermission):

    def has_permission(self, request, view):
        try:
            user_id = request.user.id
            user = AuthUser.objects.get(id=user_id)
            role_id = user.role.id
            role = Role.objects.get(id=role_id)
            if role.user_role == 'admin' or role.user_role == 'super':
                return True
            return False
        except ObjectDoesNotExist as e:
            return False


class PostPermission(BasePermission):
    """
    a custom permission class: to authorize request for post
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return False


class UserAdminPermission(BasePermission):
    """
    a custom permission class: to authorize user or admin for access
    """

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user
            role_id = user.role.id
            role = Role.objects.get(id=role_id)
            if role.user_role == 'admin':
                return True
            return obj == request.user
        except ObjectDoesNotExist as e:
            return False


class UserPostPermission(BasePermission):
    """
    a custom permission class: to authorize user for creating document
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            doc_user_id = int(request.data['user'])
            return request.user.id == doc_user_id
        return False


class GetPermission(BasePermission):
    """
    a custom permission class
    """
    def has_permission(self, request, view):
        return request.method == "GET"


class UserRetrievePermission(BasePermission):
    """
    a custom permission class: to authorize user for retrieving document
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.user_id == request.user.id
        return False
