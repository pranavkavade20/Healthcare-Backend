from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Doctor model.
    """
    list_display = [
        'id',
        'full_name',
        'specialization',
        'license_number',
        'experience_years',
        'city',
        'consultation_fee',
        'is_available',
        'is_active',
        'created_by',
        'created_at'
    ]
    
    list_filter = [
        'specialization',
        'gender',
        'is_active',
        'is_available',
        'city',
        'state',
        'created_at'
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'license_number',
        'qualification',
        'clinic_name',
        'created_by__email'
    ]
    
    readonly_fields = [
        'id',
        'full_name',
        'age',
        'full_address',
        'created_by',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'age', 'gender')
        }),
        ('Professional Information', {
            'fields': (
                'specialization',
                'qualification',
                'license_number',
                'experience_years'
            )
        }),
        ('Clinic/Hospital Information', {
            'fields': (
                'clinic_name',
                'clinic_address',
                'city',
                'state',
                'postal_code',
                'country',
                'full_address'
            )
        }),
        ('Consultation Details', {
            'fields': (
                'consultation_fee',
                'available_days',
                'available_time',
                'is_available'
            )
        }),
        ('Additional Information', {
            'fields': ('bio', 'languages_spoken'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    list_per_page = 25
    
    def full_name(self, obj):
        """Display full name in list view."""
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def age(self, obj):
        """Display age in detail view."""
        return obj.age
    age.short_description = 'Age'
    
    def full_address(self, obj):
        """Display full address in detail view."""
        return obj.full_address
    full_address.short_description = 'Complete Address'