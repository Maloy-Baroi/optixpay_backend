# app_auth/serializers.py
import random

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from app_auth.models import CustomUser, CustomGroup, CustomPermission  # Correct path to the CustomUser model


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = CustomUser.objects._create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False  # User is not active until they verify their email
        )
        # Generate and store OTP somewhere, e.g., in cache or a model
        otp = random.randint(1000, 9999)
        self.context['otp'] = otp  # Save OTP to context for use in the view
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'referral', 'create_date', 'write_date', 'is_staff',
                  'is_active']

        extra_kwargs = {
            'referral': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser.objects._create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']


class PermissionSerializer(serializers.ModelSerializer):
    inclusive_models = ContentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = CustomPermission
        fields = ['id', 'permission_name', 'inclusive_models', 'permission_type']


class GroupSerializer(serializers.ModelSerializer):
    all_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = CustomGroup
        fields = [
            'id', 'name', 'all_permissions'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'all_permissions': {'required': False},
        }
