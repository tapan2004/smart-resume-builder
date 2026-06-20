from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'role']
