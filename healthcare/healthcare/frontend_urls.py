"""
Frontend URLs for Healthcare System
"""
from django.urls import path
from healthcare.frontend_views import (
    # Dashboard
    dashboard_view,
    
    # Patients
    patient_list_view,
    patient_detail_view,
    patient_create_view,
    patient_edit_view,
    patient_delete_view,
    
    # Doctors
    doctor_list_view,
    doctor_detail_view,
    doctor_create_view,
    doctor_edit_view,
    doctor_delete_view,
    
    # Mappings
    mapping_list_view,
    mapping_create_view,
    mapping_edit_view,
    mapping_delete_view,
    
    # Auth
    login_view,
    register_view,
    logout_view,
    profile_view,
    settings_view,
)

urlpatterns = [
    # Dashboard
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard-alt'),
    
    # Patients
    path('patients/', patient_list_view, name='patient-list'),
    path('patients/<int:pk>/', patient_detail_view, name='patient-detail'),
    path('patients/create/', patient_create_view, name='patient-create'),
    path('patients/<int:pk>/edit/', patient_edit_view, name='patient-edit'),
    path('patients/<int:pk>/delete/', patient_delete_view, name='patient-delete'),
    
    # Doctors
    path('doctors/', doctor_list_view, name='doctor-list'),
    path('doctors/<int:pk>/', doctor_detail_view, name='doctor-detail'),
    path('doctors/create/', doctor_create_view, name='doctor-create'),
    path('doctors/<int:pk>/edit/', doctor_edit_view, name='doctor-edit'),
    path('doctors/<int:pk>/delete/', doctor_delete_view, name='doctor-delete'),
    
    # Mappings
    path('mappings/', mapping_list_view, name='mapping-list'),
    path('mappings/create/', mapping_create_view, name='mapping-create'),
    path('mappings/<int:pk>/edit/', mapping_edit_view, name='mapping-edit'),
    path('mappings/<int:pk>/delete/', mapping_delete_view, name='mapping-delete'),
    
    # Auth
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile_view, name='profile'),
    path('auth/settings/', settings_view, name='settings'),
]
