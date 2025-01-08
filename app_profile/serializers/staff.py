from rest_framework import serializers

from app_profile.models.staff import StaffProfile


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = [
            'user',
            'name',
            'phone_number',
            'unique_id',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
