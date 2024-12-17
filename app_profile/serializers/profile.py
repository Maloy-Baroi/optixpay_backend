from rest_framework import serializers

from app_profile.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # Custom fields for validation
    country_display = serializers.CharField(source='get_country_display', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'profile_type',
            'user',
            'full_name',
            'country',
            'country_display',
            'phone_number',
            'telegram',
            'document_type',
            'document_type_display',
            'front_side',
            'back_side',
            'selfie_with_id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'is_active'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']

    def validate_phone_number(self, value):
        """Custom validation for Bangladeshi phone numbers."""
        if not value.startswith('+88') and not value.startswith('01'):
            raise serializers.ValidationError("Phone number must start with '+88' or '01'.")
        return value

    def validate(self, attrs):
        """
        Object-level validation to check file upload constraints or
        perform additional checks between fields.
        """
        # Determine if this is a create or update request
        request = self.context.get('request', None)
        if request and request.method == 'POST':  # Only validate on create (POST)
            front_side = attrs.get('front_side')
            selfie_with_id = attrs.get('selfie_with_id')

            # Ensure all required files are uploaded
            if not front_side or not selfie_with_id:
                raise serializers.ValidationError("Front side and selfie with ID are mandatory.")

        # Check file size limit (e.g., max 5MB per file)
        max_file_size = 5 * 1024 * 1024  # 5MB in bytes
        for file_field in ['front_side', 'back_side', 'selfie_with_id']:
            file = attrs.get(file_field)
            if file and file.size > max_file_size:
                raise serializers.ValidationError(
                    f"The file '{file_field}' exceeds the 5MB size limit."
                )

        return attrs

    def create(self, validated_data):
        """
        Custom create method for creating a profile.
        """
        user = self.context['request'].user  # Get the user from the request
        validated_data['created_by'] = user
        validated_data['user'] = user
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        """
        Custom update method for updating a profile.
        """
        user = self.context['request'].user  # Get the user from the request
        validated_data['updated_by'] = user
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
