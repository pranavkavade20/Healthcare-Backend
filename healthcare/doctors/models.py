from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date


class Doctor(models.Model):
    """
    Doctor model to store doctor/physician information.
    Each doctor is associated with a user (creator) who added them to the system.
    """
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('ENDOCRINOLOGY', 'Endocrinology'),
        ('GASTROENTEROLOGY', 'Gastroenterology'),
        ('GENERAL_PRACTICE', 'General Practice'),
        ('GYNECOLOGY', 'Gynecology'),
        ('NEUROLOGY', 'Neurology'),
        ('ONCOLOGY', 'Oncology'),
        ('OPHTHALMOLOGY', 'Ophthalmology'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('PEDIATRICS', 'Pediatrics'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('RADIOLOGY', 'Radiology'),
        ('SURGERY', 'Surgery'),
        ('UROLOGY', 'Urology'),
        ('OTHER', 'Other'),
    ]
    
    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # License number validator
    license_regex = RegexValidator(
        regex=r'^[A-Z0-9]{5,20}$',
        message="License number must be 5-20 characters long and contain only uppercase letters and numbers."
    )
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text="Phone number in format: '+999999999'"
    )
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Professional Information
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES
    )
    qualification = models.CharField(
        max_length=200,
        help_text="e.g., MBBS, MD, MS, etc."
    )
    license_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[license_regex],
        help_text="Medical license/registration number"
    )
    experience_years = models.PositiveIntegerField(
        validators=[MaxValueValidator(60)],
        help_text="Years of experience"
    )
    
    # Contact Information
    clinic_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the clinic/hospital"
    )
    clinic_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Additional Information
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Consultation fee in local currency"
    )
    available_days = models.CharField(
        max_length=200,
        help_text="e.g., Monday to Friday, Weekdays, etc."
    )
    available_time = models.CharField(
        max_length=100,
        help_text="e.g., 9:00 AM - 5:00 PM"
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Brief biography or professional summary"
    )
    
    languages_spoken = models.CharField(
        max_length=200,
        default='English',
        help_text="Comma-separated list of languages"
    )
    
    # System Fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctors'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(
        default=True,
        help_text="Currently accepting new patients"
    )
    
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['specialization', 'is_active']),
            models.Index(fields=['city', 'specialization']),
            models.Index(fields=['email']),
            models.Index(fields=['license_number']),
        ]
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.get_specialization_display()}"
    
    @property
    def full_name(self):
        """Return doctor's full name with title."""
        return f"Dr. {self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate and return doctor's age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def full_address(self):
        """Return complete formatted address."""
        address_parts = [
            self.clinic_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ", ".join(filter(None, address_parts))
    
    def clean(self):
        """Validate model data."""
        from django.core.exceptions import ValidationError
        
        # Validate date of birth is not in the future
        if self.date_of_birth > date.today():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})
        
        # Validate age is reasonable (at least 23 years old for a doctor)
        age = date.today().year - self.date_of_birth.year
        if age < 23:
            raise ValidationError({
                'date_of_birth': 'Doctor must be at least 23 years old (minimum age to complete medical degree).'
            })
        if age > 100:
            raise ValidationError({'date_of_birth': 'Please enter a valid date of birth.'})
        
        # Validate experience years doesn't exceed age - 23
        if self.experience_years > (age - 23):
            raise ValidationError({
                'experience_years': f'Experience years cannot exceed {age - 23} years based on age.'
            })
        
        # Validate consultation fee
        if self.consultation_fee < 0:
            raise ValidationError({'consultation_fee': 'Consultation fee cannot be negative.'})
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean before saving."""
        self.full_clean()
        # Convert license number to uppercase
        self.license_number = self.license_number.upper()
        super().save(*args, **kwargs)