from django.http import HttpResponse
from django.shortcuts import loader, redirect
from rest_framework import status
from rest_framework.views import APIView
from .models import AuthUser
from .serializers import AuthUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import RetrieveUpdateDestroyAPIView

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        template = loader.get_template("index.html")
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


class AuthUserListView(APIView):
    """
    a class based view: to list all the user data, JWTAuthentication is applied
    """
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    serializer_class = AuthUserSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        snippet = self.get_object()
        serialized = AuthUserSerializer(snippet)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        snippet.delete()
        serialized = AuthUserSerializer(snippet)
        return JsonResponse(serialized.data)
