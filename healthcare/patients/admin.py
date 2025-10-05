from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model.
    """
    list_display = [
        'id',
        'full_name',
        'phone',
        'email',
        'gender',
        'age',
        'city',
        'created_by',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'gender',
        'blood_group',
        'is_active',
        'city',
        'state',
        'created_at'
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'phone',
        'email',
        'created_by__email'
    ]
    
    readonly_fields = [
        'id',
        'full_name',
        'age',
        'created_by',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'age', 'gender', 'blood_group')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name',
                'emergency_contact_phone',
                'emergency_contact_relation'
            )
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
        """Display age in list view."""
        return obj.age
    age.short_description = 'Age'