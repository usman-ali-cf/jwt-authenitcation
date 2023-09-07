from rest_framework import serializers
from .models import AuthUser


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ['id', 'name', 'email', 'gender', 'city', 'is_admin', 'password', 'last_login']

    extra_kwargs = {
        'password': {'write_only': True}
    }

    def create(self, validated_data):
        user = AuthUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            city=validated_data['city'],
            is_admin=validated_data['is_admin'],
            last_login=validated_data['last_login']
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
