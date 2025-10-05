from django.urls import path
from .views import (
    PatientDoctorMappingListCreateView,
    PatientDoctorsView,
    PatientDoctorMappingDetailView
)

app_name = 'mappings'

urlpatterns = [
    # List all mappings and create new mapping
    path('', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    
    # Get all doctors for a specific patient
    path('<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
    
    # Manage specific mapping (get, update, delete)
    path('detail/<int:pk>/', PatientDoctorMappingDetailView.as_view(), name='mapping-detail'),
]