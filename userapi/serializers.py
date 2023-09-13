from rest_framework import serializers
from .models import AuthUser, Role, Document
from django.core.exceptions import ObjectDoesNotExist


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ['id', 'name', 'email', 'gender', 'city', 'password', 'role', 'lead']

    extra_kwargs = {
        'password': {'write_only': True}
    }

    def create(self, validated_data):
        user = AuthUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        try:
            user = super().update(instance, validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        except ObjectDoesNotExist as e:
            print('User Not found: ', e)
            return None


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['user_role', 'description']


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"
