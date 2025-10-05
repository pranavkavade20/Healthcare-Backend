from rest_framework import serializers
from datetime import date
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model with comprehensive validation.
    """
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    full_address = serializers.CharField(read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
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
            'specialization',
            'specialization_display',
            'qualification',
            'license_number',
            'experience_years',
            'clinic_name',
            'clinic_address',
            'city',
            'state',
            'postal_code',
            'country',
            'full_address',
            'consultation_fee',
            'available_days',
            'available_time',
            'bio',
            'languages_spoken',
            'is_active',
            'is_available',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at', 
            'full_name', 
            'age', 
            'full_address',
            'created_by_email',
            'specialization_display'
        ]
    
    def validate_first_name(self, value):
        """Validate first name."""
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        if not value.replace(' ', '').replace('.', '').isalpha():
            raise serializers.ValidationError("First name should only contain letters.")
        return value.strip().title()
    
    def validate_last_name(self, value):
        """Validate last name."""
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not value.replace(' ', '').replace('.', '').isalpha():
            raise serializers.ValidationError("Last name should only contain letters.")
        return value.strip().title()
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if not value.strip():
            raise serializers.ValidationError("Email is required.")
        
        email = value.lower().strip()
        
        # Check if email already exists (excluding current instance for updates)
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.filter(email=email).exclude(id=doctor_id).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        
        return email
    
    def validate_date_of_birth(self, value):
        """Validate date of birth."""
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        # Calculate age
        age = date.today().year - value.year - (
            (date.today().month, date.today().day) < (value.month, value.day)
        )
        
        if age < 23:
            raise serializers.ValidationError(
                "Doctor must be at least 23 years old (minimum age to complete medical degree)."
            )
        if age > 100:
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
    
    def validate_license_number(self, value):
        """Validate license number."""
        if not value.strip():
            raise serializers.ValidationError("License number is required.")
        
        # Convert to uppercase and remove spaces
        license_num = value.strip().upper().replace(' ', '')
        
        if len(license_num) < 5 or len(license_num) > 20:
            raise serializers.ValidationError(
                "License number must be between 5 and 20 characters."
            )
        
        if not license_num.isalnum():
            raise serializers.ValidationError(
                "License number should only contain letters and numbers."
            )
        
        # Check if license number already exists (excluding current instance)
        doctor_id = self.instance.id if self.instance else None
        if Doctor.objects.filter(license_number=license_num).exclude(id=doctor_id).exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        
        return license_num
    
    def validate_qualification(self, value):
        """Validate qualification."""
        if not value.strip():
            raise serializers.ValidationError("Qualification is required.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Qualification must be at least 2 characters long.")
        return value.strip()
    
    def validate_experience_years(self, value):
        """Validate experience years."""
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative.")
        if value > 60:
            raise serializers.ValidationError("Experience years cannot exceed 60 years.")
        return value
    
    def validate_consultation_fee(self, value):
        """Validate consultation fee."""
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative.")
        if value > 100000:
            raise serializers.ValidationError("Consultation fee seems unusually high. Please verify.")
        return value
    
    def validate_clinic_address(self, value):
        """Validate clinic address."""
        if not value.strip():
            raise serializers.ValidationError("Clinic address is required.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a complete clinic address.")
        return value.strip()
    
    def validate_city(self, value):
        """Validate city."""
        if not value.strip():
            raise serializers.ValidationError("City is required.")
        return value.strip().title()
    
    def validate_state(self, value):
        """Validate state."""
        if not value.strip():
            raise serializers.ValidationError("State is required.")
        return value.strip().title()
    
    def validate_postal_code(self, value):
        """Validate postal code."""
        if not value.strip():
            raise serializers.ValidationError("Postal code is required.")
        return value.strip()
    
    def validate_available_days(self, value):
        """Validate available days."""
        if not value.strip():
            raise serializers.ValidationError("Available days are required.")
        return value.strip()
    
    def validate_available_time(self, value):
        """Validate available time."""
        if not value.strip():
            raise serializers.ValidationError("Available time is required.")
        return value.strip()
    
    def validate(self, attrs):
        """Cross-field validation."""
        # Validate experience years against age if date_of_birth is provided
        if 'date_of_birth' in attrs and 'experience_years' in attrs:
            dob = attrs['date_of_birth']
            age = date.today().year - dob.year
            experience = attrs['experience_years']
            
            if experience > (age - 23):
                raise serializers.ValidationError({
                    'experience_years': f'Experience years cannot exceed {age - 23} years based on age.'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Create doctor with the authenticated user as creator."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing doctors.
    """
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id',
            'full_name',
            'specialization',
            'specialization_display',
            'qualification',
            'experience_years',
            'city',
            'consultation_fee',
            'phone',
            'email',
            'is_available',
            'is_active',
            'created_at',
        ]
        read_only_fields = fields


class DoctorUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating doctor information.
    Reuses validation from DoctorSerializer.
    """
    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'specialization',
            'qualification',
            'license_number',
            'experience_years',
            'clinic_name',
            'clinic_address',
            'city',
            'state',
            'postal_code',
            'country',
            'consultation_fee',
            'available_days',
            'available_time',
            'bio',
            'languages_spoken',
            'is_active',
            'is_available',
        ]
    
    # Reuse validation methods from DoctorSerializer
    validate_first_name = DoctorSerializer.validate_first_name
    validate_last_name = DoctorSerializer.validate_last_name
    validate_email = DoctorSerializer.validate_email
    validate_date_of_birth = DoctorSerializer.validate_date_of_birth
    validate_phone = DoctorSerializer.validate_phone
    validate_license_number = DoctorSerializer.validate_license_number
    validate_qualification = DoctorSerializer.validate_qualification
    validate_experience_years = DoctorSerializer.validate_experience_years
    validate_consultation_fee = DoctorSerializer.validate_consultation_fee
    validate_clinic_address = DoctorSerializer.validate_clinic_address
    validate_city = DoctorSerializer.validate_city
    validate_state = DoctorSerializer.validate_state
    validate_postal_code = DoctorSerializer.validate_postal_code
    validate_available_days = DoctorSerializer.validate_available_days
    validate_available_time = DoctorSerializer.validate_available_time
    validate = DoctorSerializer.validate