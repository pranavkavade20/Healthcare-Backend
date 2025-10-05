from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDoctorMapping model.
    """
    list_display = [
        'id',
        'patient_name',
        'doctor_name',
        'doctor_specialization',
        'assigned_date',
        'status',
        'created_by',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'assigned_date',
        'created_at',
        'doctor__specialization'
    ]
    
    search_fields = [
        'patient__first_name',
        'patient__last_name',
        'doctor__first_name',
        'doctor__last_name',
        'doctor__specialization',
        'created_by__email'
    ]
    
    readonly_fields = [
        'id',
        'assigned_date',
        'created_by',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Mapping Information', {
            'fields': ('patient', 'doctor', 'assigned_date', 'status')
        }),
        ('Details', {
            'fields': ('reason', 'notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    list_per_page = 25
    
    def patient_name(self, obj):
        """Display patient name in list view."""
        return obj.patient.full_name
    patient_name.short_description = 'Patient'
    patient_name.admin_order_field = 'patient__first_name'
    
    def doctor_name(self, obj):
        """Display doctor name in list view."""
        return obj.doctor.full_name
    doctor_name.short_description = 'Doctor'
    doctor_name.admin_order_field = 'doctor__first_name'
    
    def doctor_specialization(self, obj):
        """Display doctor specialization in list view."""
        return obj.doctor.get_specialization_display()
    doctor_specialization.short_description = 'Specialization'
    doctor_specialization.admin_order_field = 'doctor__specialization'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('patient', 'doctor', 'created_by')