from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientBasicSerializer(serializers.ModelSerializer):
    """Basic patient information for mapping responses."""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'age', 'phone', 'email', 'gender', 'city']
        read_only_fields = fields


class DoctorBasicSerializer(serializers.ModelSerializer):
    """Basic doctor information for mapping responses."""
    full_name = serializers.CharField(read_only=True)
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
            'phone',
            'email',
            'city',
            'consultation_fee'
        ]
        read_only_fields = fields


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient-Doctor Mapping with full details.
    """
    patient_details = PatientBasicSerializer(source='patient', read_only=True)
    doctor_details = DoctorBasicSerializer(source='doctor', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'patient_details',
            'doctor',
            'doctor_details',
            'assigned_date',
            'status',
            'status_display',
            'reason',
            'notes',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'assigned_date',
            'created_by_email',
            'created_at',
            'updated_at',
            'patient_details',
            'doctor_details',
            'status_display'
        ]
    
    def validate_patient(self, value):
        """Validate patient exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Cannot assign doctor to an inactive patient.")
        
        # Check if the user owns this patient
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError(
                "You can only assign doctors to your own patients."
            )
        
        return value
    
    def validate_doctor(self, value):
        """Validate doctor exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Cannot assign an inactive doctor.")
        
        if not value.is_available:
            raise serializers.ValidationError(
                "This doctor is currently not accepting new patients."
            )
        
        return value
    
    def validate(self, attrs):
        """Cross-field validation."""
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if mapping already exists (for create operation)
        if not self.instance:  # Only for creation
            if PatientDoctorMapping.objects.filter(
                patient=patient,
                doctor=doctor
            ).exists():
                raise serializers.ValidationError({
                    'non_field_errors': [
                        f"Doctor {doctor.full_name} is already assigned to patient {patient.full_name}."
                    ]
                })
        
        return attrs
    
    def create(self, validated_data):
        """Create mapping with the authenticated user as creator."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing mappings.
    """
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(
        source='doctor.get_specialization_display',
        read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'patient_name',
            'doctor',
            'doctor_name',
            'doctor_specialization',
            'assigned_date',
            'status',
            'status_display',
            'created_at',
        ]
        read_only_fields = fields


class PatientDoctorMappingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating mapping status and notes.
    """
    class Meta:
        model = PatientDoctorMapping
        fields = ['status', 'reason', 'notes']
    
    def validate_status(self, value):
        """Validate status transitions."""
        if self.instance:
            current_status = self.instance.status
            
            # Define valid status transitions
            valid_transitions = {
                'ACTIVE': ['INACTIVE', 'COMPLETED'],
                'INACTIVE': ['ACTIVE', 'COMPLETED'],
                'COMPLETED': []  # Cannot change from COMPLETED
            }
            
            if current_status == 'COMPLETED' and value != 'COMPLETED':
                raise serializers.ValidationError(
                    "Cannot change status from COMPLETED to another status."
                )
            
            if value not in valid_transitions.get(current_status, []) and value != current_status:
                raise serializers.ValidationError(
                    f"Invalid status transition from {current_status} to {value}."
                )
        
        return value