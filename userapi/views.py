from django.http import HttpResponse
from django.shortcuts import loader, redirect
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import AuthUser, Document, Role
from .serializers import AuthUserSerializer, DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from django.views import View
from .users_permissions import (
    AdminAccess, UserAdminPermission,
    UserPostPermission, UserRetrievePermission,
    PostPermission, GetPermission
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# Create your views here.


class LoginViewToken(TokenObtainPairView):
    """
    a class based view: to authenticate the user and generate jwt token
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Check if authentication was successful
        if response.status_code == 200:
            token = response.data.get('access')

            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
            )

        return response


class Home(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        template = loader.get_template("index.html")
        return HttpResponse(template.render())


class AdminHome(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminAccess]

    def get(self, request):
        template = loader.get_template("admin_index.html")
        return HttpResponse(template.render())


class EditUserForm(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        template = loader.get_template("edit_user.html")
        return HttpResponse(template.render())


class LoginFormView(View):

    def get(self, request):
        template = loader.get_template("login.html")
        context = {}
        return HttpResponse(template.render(context, request))


class RegisterFormView(View):

    def get(self, request):
        template = loader.get_template("register.html")
        context = {}
        return HttpResponse(template.render(context, request))


class UserViewSet(viewsets.ModelViewSet):
    """
    View to list and create users in the system.

    * Requires JWT authentication.
    * Only admin users are able to access all users.
    * Anyone can create user
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = AuthUserSerializer
    queryset = AuthUser.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated, AdminAccess | PostPermission]
        else:
            permission_classes = [IsAuthenticated, UserAdminPermission]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'], permission_classes=[AdminAccess])
    def add_lead(self, request, id):
        try:
            user = self.get_object()
            lead_list = request.data['lead']
            leads = []
            for lead in lead_list:
                leads.append(AuthUser.objects.get(id=lead))
            user.lead.set(leads)
            user.save()
            return Response(data={"detail": "Success"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"details": "Lead User does not exists"}, status=status.HTTP_400_BAD_REQUEST)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    View to list and create document in the system.

    * Requires JWT authentication.
    * admin users are able to access all documents.
    * user is able to create and view his/her own documents
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = DocumentSerializer
    lookup_field = "id"

    def get_queryset(self):
        try:
            user = self.request.user
            role_id = user.role.id
            role = Role.objects.get(id=role_id)
            if role.user_role == 'admin' or role.user_role == 'super':
                return Document.objects.all()
            return Document.objects.filter(user=user.id)
        except ObjectDoesNotExist as e:
            return Document.objects.none()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated, AdminAccess | UserPostPermission | GetPermission]
        else:
            permission_classes = [IsAuthenticated, AdminAccess | UserRetrievePermission]
        return [permission() for permission in permission_classes]
