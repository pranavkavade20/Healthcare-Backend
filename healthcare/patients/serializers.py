from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from datetime import date
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model with comprehensive validation.
    """
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'date_of_birth',
            'age',
            'gender',
            'blood_group',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'medical_history',
            'allergies',
            'current_medications',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            'is_active',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'age', 'created_by_email']
    
    def validate_first_name(self, value):
        """Validate first name."""
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("First name should only contain letters.")
        return value.strip().title()
    
    def validate_last_name(self, value):
        """Validate last name."""
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Last name should only contain letters.")
        return value.strip().title()
    
    def validate_email(self, value):
        """Validate email if provided."""
        if value and not value.strip():
            return None
        return value.lower() if value else None
    
    def validate_date_of_birth(self, value):
        """Validate date of birth."""
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        # Calculate age
        age = date.today().year - value.year - (
            (date.today().month, date.today().day) < (value.month, value.day)
        )
        
        if age < 0 or age > 150:
            raise serializers.ValidationError("Please enter a valid date of birth.")
        
        return value
    
    def validate_phone(self, value):
        """Validate phone number."""
        # Remove spaces and special characters except +
        cleaned_phone = ''.join(filter(lambda x: x.isdigit() or x == '+', value))
        
        if not cleaned_phone:
            raise serializers.ValidationError("Phone number is required.")
        
        # Check if phone starts with + and has valid length
        if cleaned_phone.startswith('+'):
            if len(cleaned_phone) < 10 or len(cleaned_phone) > 16:
                raise serializers.ValidationError(
                    "Phone number with country code must be between 10 and 16 digits."
                )
        else:
            if len(cleaned_phone) < 10 or len(cleaned_phone) > 15:
                raise serializers.ValidationError(
                    "Phone number must be between 10 and 15 digits."
                )
        
        return cleaned_phone
    
    def validate_emergency_contact_phone(self, value):
        """Validate emergency contact phone."""
        return self.validate_phone(value)
    
    def validate_postal_code(self, value):
        """Validate postal code."""
        if not value.strip():
            raise serializers.ValidationError("Postal code is required.")
        return value.strip()
    
    def validate_emergency_contact_name(self, value):
        """Validate emergency contact name."""
        if not value.strip():
            raise serializers.ValidationError("Emergency contact name is required.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Emergency contact name must be at least 2 characters long."
            )
        return value.strip().title()
    
    def validate(self, attrs):
        """Cross-field validation."""
        # Ensure emergency contact phone is different from patient phone
        if 'phone' in attrs and 'emergency_contact_phone' in attrs:
            if attrs['phone'] == attrs['emergency_contact_phone']:
                raise serializers.ValidationError({
                    'emergency_contact_phone': 
                    'Emergency contact phone should be different from patient phone.'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Create patient with the authenticated user as creator."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class PatientListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing patients.
    """
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'age',
            'gender',
            'city',
            'is_active',
            'created_at',
        ]
        read_only_fields = fields


class PatientUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating patient information.
    Reuses validation from PatientSerializer.
    """
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'blood_group',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'medical_history',
            'allergies',
            'current_medications',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            'is_active',
        ]
    
    # Reuse validation methods from PatientSerializer
    validate_first_name = PatientSerializer.validate_first_name
    validate_last_name = PatientSerializer.validate_last_name
    validate_email = PatientSerializer.validate_email
    validate_date_of_birth = PatientSerializer.validate_date_of_birth
    validate_phone = PatientSerializer.validate_phone
    validate_emergency_contact_phone = PatientSerializer.validate_emergency_contact_phone
    validate_postal_code = PatientSerializer.validate_postal_code
    validate_emergency_contact_name = PatientSerializer.validate_emergency_contact_name
    validate = PatientSerializer.validate