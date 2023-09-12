from rest_framework import serializers
from .models import AuthUser, Role, Document


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ['id', 'name', 'email', 'gender', 'city', 'password', 'role']

    extra_kwargs = {
        'password': {'write_only': True}
    }

    def create(self, validated_data):
        role_instance = Role.objects.get(id=validated_data['role'].id)

        user = AuthUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            city=validated_data['city'],
            role=role_instance,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['user_role', 'description']


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"
