from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import AuthUser
from .serializers import AuthUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# Create your views here.


class LoginViewToken(TokenObtainPairView):
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


def home(request):
    return HttpResponse("Hello")


class RegisterView(APIView):

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AuthUserEditView(RetrieveUpdateDestroyAPIView):
    queryset = AuthUser.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AuthUserSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        snippet = self.get_object()
        serialized = AuthUserSerializer(snippet)
        return JsonResponse(serialized.data)

    def partial_update(self, request, *args, **kwargs):
        snippet = self.get_object()
        data = JSONParser().parse(request)
        serialized = AuthUserSerializer(snippet, data=data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data, status=status.HTTP_200_OK)
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        snippet.delete()
        serialized = AuthUserSerializer(snippet)
        return JsonResponse(serialized.data)


class AuthUserListView(APIView):
    authentication_classes = [JWTAuthentication]
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
