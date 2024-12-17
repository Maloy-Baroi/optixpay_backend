# from rest_framework import serializers
# from app_bank.models.bank import BankModel, BankTypeModel




# class BankTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankTypeModel
#         fields = '__all__'

#     def validate_name(self, value):
#         """
#         Ensure the name is not blank and follows specific rules.
#         """
#         if not value.strip():
#             raise serializers.ValidationError("The name cannot be empty or whitespace.")
#         # if not value.isalnum():
#         #     raise serializers.ValidationError("The name must contain only alphanumeric characters.")
#         return value

#     def validate_category(self, value):
#         """
#         Ensure the category is one of the allowed choices.
#         """
#         valid_choices = [choice[0] for choice in BankTypeModel.CATEGORY_CHOICES]
#         if value not in valid_choices:
#             raise serializers.ValidationError(f"Invalid category. Valid choices are: {valid_choices}")
#         return value


















from rest_framework import serializers
from app_bank.models.bank import BankTypeModel

class BankTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTypeModel
        exclude = ['created_by', 'updated_by']  # Exclude these fields from the input

    def create(self, validated_data):
        # Set created_by and updated_by to the current user
        user = self.context['request'].user
        
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Set updated_by to the current user (created_by should not change on update)
        user = self.context['request'].user
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)


# from rest_framework import serializers
# from app_bank.models.bank import BankTypeModel

# class BankTypeModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankTypeModel
#         # Explicitly list the fields to ensure that is_active is included
#         fields = ['id', 'name', 'category', 'is_active']  # Ensure 'is_active' is listed

#     def create(self, validated_data):
#         # Automatically set created_by and updated_by to the current user during creation
#         user = self.context['request'].user
#         validated_data['created_by'] = user
#         validated_data['updated_by'] = user
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # Automatically set updated_by to the current user during updates
#         user = self.context['request'].user
#         validated_data['updated_by'] = user
#         return super().update(instance, validated_data)

