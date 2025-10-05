from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date


class Patient(models.Model):
    """
    Patient model to store patient information.
    Each patient is associated with a user (creator).
    """
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text="Phone number in format: '+999999999'"
    )
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        blank=True,
        null=True
    )
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Medical Information
    medical_history = models.TextField(
        blank=True,
        null=True,
        help_text="Brief medical history of the patient"
    )
    allergies = models.TextField(
        blank=True,
        null=True,
        help_text="Known allergies"
    )
    current_medications = models.TextField(
        blank=True,
        null=True,
        help_text="Current medications being taken"
    )
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(
        validators=[phone_regex],
        max_length=17
    )
    emergency_contact_relation = models.CharField(max_length=50)
    
    # System Fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'is_active']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"
    
    @property
    def full_name(self):
        """Return patient's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate and return patient's age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def clean(self):
        """Validate model data."""
        from django.core.exceptions import ValidationError
        
        # Validate date of birth is not in the future
        if self.date_of_birth > date.today():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})
        
        # Validate age is reasonable (between 0 and 150 years)
        age = date.today().year - self.date_of_birth.year
        if age < 0 or age > 150:
            raise ValidationError({'date_of_birth': 'Please enter a valid date of birth.'})
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean before saving."""
        self.full_clean()
        super().save(*args, **kwargs)