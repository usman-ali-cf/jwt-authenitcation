from rest_framework import serializers
from .models import AuthUser


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ['name', 'email', 'gender', 'city', 'is_admin', 'password', 'last_login']

    extra_kwargs = {
        'password': {'write_only': True}
    }

    def create(self, validated_data):
        user = AuthUser.objects.create(email=validated_data['email'],name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user
