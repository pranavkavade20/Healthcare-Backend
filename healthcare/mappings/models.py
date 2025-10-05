from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Model to manage patient-doctor relationships.
    Maps which doctors are assigned to which patients.
    """
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]
    
    # Relationship fields
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings'
    )
    
    # Assignment details
    assigned_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    
    # Additional information
    reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for assignment or medical condition"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the assignment"
    )
    
    # System fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_mappings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patient_doctor_mappings'
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        ordering = ['-created_at']
        
        # Ensure unique patient-doctor combination
        unique_together = ['patient', 'doctor']
        
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['doctor', 'status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['assigned_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} -> {self.doctor.full_name}"
    
    def clean(self):
        """Validate model data."""
        # Check if patient is active
        if not self.patient.is_active:
            raise ValidationError({
                'patient': 'Cannot assign doctor to an inactive patient.'
            })
        
        # Check if doctor is active
        if not self.doctor.is_active:
            raise ValidationError({
                'doctor': 'Cannot assign an inactive doctor to a patient.'
            })
        
        # Check if doctor is available
        if not self.doctor.is_available and self.status == 'ACTIVE':
            raise ValidationError({
                'doctor': 'This doctor is currently not accepting new patients.'
            })
        
        # Check if patient and doctor belong to the same user (creator)
        # This ensures users can only map their own patients to doctors
        if hasattr(self, 'created_by'):
            if self.patient.created_by != self.created_by:
                raise ValidationError({
                    'patient': 'You can only assign doctors to your own patients.'
                })
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean before saving."""
        self.full_clean()
        super().save(*args, **kwargs)