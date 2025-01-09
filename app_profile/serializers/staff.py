from rest_framework import serializers

from app_profile.models.staff import StaffProfile


class StaffSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()

    class Meta:
        model = StaffProfile
        fields = [
            'user',
            'name',
            'phone_number',
            'unique_id',
            'authorization_details',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        extra_kwargs = {
            'user': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'unique_id': {'read_only': True},
        }

    def get_authorization_details(self, obj):
        # Only return non-sensitive information related to authorization
        return {
            "email": obj.user.email,
            "username": obj.user.username,
        }
