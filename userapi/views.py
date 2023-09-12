from django.http import HttpResponse
from django.shortcuts import loader, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from .models import AuthUser, Document
from .serializers import AuthUserSerializer, DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from .users_permissions import (
    AdminAccess, UserAdminPermission, SuperAdmin,
    UserPostPermission, UserRetrievePermission,
    PostPermission, GetPermission
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken

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


class RegisterView(APIView):
    """
    a class based view: to create new user by using serializer
    """

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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


class UsersList(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminAccess]

    def get(self, request):
        template = loader.get_template("users_list.html")
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


class AuthUserListView(APIView):
    """
    a class based view: to list all the user data, JWTAuthentication is applied
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminAccess | PostPermission]

    def get(self, request):
        users = AuthUser.objects.all()
        serializer = AuthUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AuthUserEditView(RetrieveUpdateDestroyAPIView):
    """
        a class based view: to edit any user data, JWTAuthentication is applied
    """
    queryset = AuthUser.objects.all()
    permission_classes = [IsAuthenticated, UserAdminPermission]
    serializer_class = AuthUserSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serialized = AuthUserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        serialized = AuthUserSerializer(user)
        return JsonResponse(serialized.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = AuthUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'details': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)


class AdminUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, SuperAdmin]

    def get(self, request):
        users = AuthUser.objects.filter(role_id=1)
        serializer = AuthUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DocumentListView(APIView):
    """
    View to list all users in the system.

    * Requires JWT authentication.
    * Only admin users are able to access this view.
    * But authenticated user can create document
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminAccess | UserPostPermission | GetPermission]

    def get(self, request):
        try:
            user_id = request.user.id
            documents = Document.objects.filter(user=user_id)
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"details": "Documents Not Found"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDocumentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminAccess]

    def get(self, request):
        try:
            documents = Document.objects.all()
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"details": "Documents Not Found"}, status=status.HTTP_200_OK)


class DocumentDetailView(RetrieveUpdateDestroyAPIView):
    """
    View Update Delete document from the system.

    * Requires JWT authentication.
    * admin users are able to access this view with all operation.
    * non-admin users can just view their documents
    """
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated, AdminAccess | UserRetrievePermission]
    serializer_class = DocumentSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()
        serialized = DocumentSerializer(document)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete()
        serialized = DocumentSerializer(document)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        document = self.get_object()
        serializer = DocumentSerializer(instance=document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
