from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from authentication.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


# Dashboard View
@login_required(login_url='login')
def dashboard_view(request):
    """Dashboard with statistics and quick actions"""
    context = {
        'total_patients': Patient.objects.filter(created_by=request.user).count(),
        'total_doctors': Doctor.objects.filter(created_by=request.user).count(),
        'total_mappings': PatientDoctorMapping.objects.filter(patient__created_by=request.user).count(),
    }
    return render(request, 'healthcare/dashboard.html', context)


# Patient Views
@login_required(login_url='login')
def patient_list_view(request):
    """List all patients with filtering"""
    patients = Patient.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Gender filter
    gender = request.GET.get('gender', '')
    if gender:
        patients = patients.filter(gender=gender)
    
    # City filter
    city = request.GET.get('city', '')
    if city:
        patients = patients.filter(city__icontains=city)
    
    # Pagination
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'patients': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'patients/patient_list.html', context)


@login_required(login_url='login')
def patient_detail_view(request, pk):
    """View patient details"""
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    context = {'patient': patient}
    return render(request, 'patients/patient_detail.html', context)


@login_required(login_url='login')
def patient_create_view(request):
    """Create new patient"""
    if request.method == 'POST':
        try:
            patient = Patient(created_by=request.user)
            patient.first_name = request.POST.get('first_name')
            patient.last_name = request.POST.get('last_name')
            patient.email = request.POST.get('email')
            patient.phone = request.POST.get('phone')
            patient.date_of_birth = request.POST.get('date_of_birth')
            patient.gender = request.POST.get('gender')
            patient.blood_group = request.POST.get('blood_group')
            patient.address = request.POST.get('address')
            patient.city = request.POST.get('city')
            patient.state = request.POST.get('state')
            patient.postal_code = request.POST.get('postal_code')
            patient.country = request.POST.get('country', 'India')
            patient.medical_history = request.POST.get('medical_history')
            patient.allergies = request.POST.get('allergies')
            patient.current_medications = request.POST.get('current_medications')
            patient.emergency_contact_name = request.POST.get('emergency_contact_name')
            patient.emergency_contact_phone = request.POST.get('emergency_contact_phone')
            patient.emergency_contact_relation = request.POST.get('emergency_contact_relation')
            patient.save()
            messages.success(request, 'Patient added successfully!')
            return redirect('patient-detail', pk=patient.pk)
        except Exception as e:
            messages.error(request, f'Error creating patient: {str(e)}')
    
    return render(request, 'patients/patient_form.html')


@login_required(login_url='login')
def patient_edit_view(request, pk):
    """Edit patient"""
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        try:
            patient.first_name = request.POST.get('first_name')
            patient.last_name = request.POST.get('last_name')
            patient.email = request.POST.get('email')
            patient.phone = request.POST.get('phone')
            patient.date_of_birth = request.POST.get('date_of_birth')
            patient.gender = request.POST.get('gender')
            patient.blood_group = request.POST.get('blood_group')
            patient.address = request.POST.get('address')
            patient.city = request.POST.get('city')
            patient.state = request.POST.get('state')
            patient.postal_code = request.POST.get('postal_code')
            patient.country = request.POST.get('country', 'India')
            patient.medical_history = request.POST.get('medical_history')
            patient.allergies = request.POST.get('allergies')
            patient.current_medications = request.POST.get('current_medications')
            patient.emergency_contact_name = request.POST.get('emergency_contact_name')
            patient.emergency_contact_phone = request.POST.get('emergency_contact_phone')
            patient.emergency_contact_relation = request.POST.get('emergency_contact_relation')
            patient.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient-detail', pk=patient.pk)
        except Exception as e:
            messages.error(request, f'Error updating patient: {str(e)}')
    
    context = {'object': patient}
    return render(request, 'patients/patient_form.html', context)


@login_required(login_url='login')
def patient_delete_view(request, pk):
    """Delete patient"""
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient-list')
    
    return render(request, 'patients/patient_confirm_delete.html', {'object': patient})


# Doctor Views
@login_required(login_url='login')
def doctor_list_view(request):
    """List all doctors with filtering"""
    doctors = Doctor.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = doctors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Specialization filter
    specialization = request.GET.get('specialization', '')
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    # City filter
    city = request.GET.get('city', '')
    if city:
        doctors = doctors.filter(city__icontains=city)
    
    # Pagination
    paginator = Paginator(doctors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'doctors/doctor_list.html', context)


@login_required(login_url='login')
def doctor_detail_view(request, pk):
    """View doctor details"""
    doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
    context = {'doctor': doctor}
    return render(request, 'doctors/doctor_detail.html', context)


@login_required(login_url='login')
def doctor_create_view(request):
    """Create new doctor"""
    if request.method == 'POST':
        try:
            doctor = Doctor(created_by=request.user)
            doctor.first_name = request.POST.get('first_name')
            doctor.last_name = request.POST.get('last_name')
            doctor.email = request.POST.get('email')
            doctor.phone = request.POST.get('phone')
            doctor.date_of_birth = request.POST.get('date_of_birth')
            doctor.gender = request.POST.get('gender')
            doctor.specialization = request.POST.get('specialization')
            doctor.qualification = request.POST.get('qualification')
            doctor.license_number = request.POST.get('license_number')
            doctor.experience_years = request.POST.get('experience_years')
            doctor.clinic_name = request.POST.get('clinic_name')
            doctor.clinic_address = request.POST.get('clinic_address')
            doctor.city = request.POST.get('city')
            doctor.state = request.POST.get('state')
            doctor.postal_code = request.POST.get('postal_code')
            doctor.country = request.POST.get('country', 'India')
            doctor.consultation_fee = request.POST.get('consultation_fee')
            doctor.available_days = request.POST.get('available_days')
            doctor.available_time = request.POST.get('available_time')
            doctor.bio = request.POST.get('bio')
            doctor.languages_spoken = request.POST.get('languages_spoken')
            doctor.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('doctor-detail', pk=doctor.pk)
        except Exception as e:
            messages.error(request, f'Error creating doctor: {str(e)}')
    
    return render(request, 'doctors/doctor_form.html')


@login_required(login_url='login')
def doctor_edit_view(request, pk):
    """Edit doctor"""
    doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        try:
            doctor.first_name = request.POST.get('first_name')
            doctor.last_name = request.POST.get('last_name')
            doctor.email = request.POST.get('email')
            doctor.phone = request.POST.get('phone')
            doctor.date_of_birth = request.POST.get('date_of_birth')
            doctor.gender = request.POST.get('gender')
            doctor.specialization = request.POST.get('specialization')
            doctor.qualification = request.POST.get('qualification')
            doctor.license_number = request.POST.get('license_number')
            doctor.experience_years = request.POST.get('experience_years')
            doctor.clinic_name = request.POST.get('clinic_name')
            doctor.clinic_address = request.POST.get('clinic_address')
            doctor.city = request.POST.get('city')
            doctor.state = request.POST.get('state')
            doctor.postal_code = request.POST.get('postal_code')
            doctor.country = request.POST.get('country', 'India')
            doctor.consultation_fee = request.POST.get('consultation_fee')
            doctor.available_days = request.POST.get('available_days')
            doctor.available_time = request.POST.get('available_time')
            doctor.bio = request.POST.get('bio')
            doctor.languages_spoken = request.POST.get('languages_spoken')
            doctor.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor-detail', pk=doctor.pk)
        except Exception as e:
            messages.error(request, f'Error updating doctor: {str(e)}')
    
    context = {'object': doctor}
    return render(request, 'doctors/doctor_form.html', context)


@login_required(login_url='login')
def doctor_delete_view(request, pk):
    """Delete doctor"""
    doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('doctor-list')
    
    return render(request, 'doctors/doctor_confirm_delete.html', {'object': doctor})


# Mapping Views
@login_required(login_url='login')
def mapping_list_view(request):
    """List all mappings with filtering"""
    mappings = PatientDoctorMapping.objects.filter(patient__created_by=request.user).order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        mappings = mappings.filter(
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query)
        )
    
    # Status filter
    status = request.GET.get('status', '')
    if status:
        mappings = mappings.filter(status=status)
    
    # Pagination
    paginator = Paginator(mappings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'mappings': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'mappings/mapping_list.html', context)


@login_required(login_url='login')
def mapping_create_view(request):
    """Create new mapping"""
    patients = Patient.objects.filter(created_by=request.user)
    doctors = Doctor.objects.filter(created_by=request.user)
    
    if request.method == 'POST':
        try:
            mapping = PatientDoctorMapping()
            mapping.patient_id = request.POST.get('patient')
            mapping.doctor_id = request.POST.get('doctor')
            mapping.reason = request.POST.get('reason')
            mapping.notes = request.POST.get('notes')
            mapping.status = 'ACTIVE'
            mapping.created_by = request.user
            mapping.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('mapping-list')
        except Exception as e:
            messages.error(request, f'Error creating assignment: {str(e)}')
    
    context = {'patients': patients, 'doctors': doctors}
    return render(request, 'mappings/mapping_form.html', context)


@login_required(login_url='login')
def mapping_edit_view(request, pk):
    """Edit mapping"""
    mapping = get_object_or_404(PatientDoctorMapping, pk=pk, patient__created_by=request.user)
    patients = Patient.objects.filter(created_by=request.user)
    doctors = Doctor.objects.filter(created_by=request.user)
    
    if request.method == 'POST':
        try:
            mapping.reason = request.POST.get('reason')
            mapping.notes = request.POST.get('notes')
            mapping.status = request.POST.get('status')
            mapping.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('mapping-list')
        except Exception as e:
            messages.error(request, f'Error updating assignment: {str(e)}')
    
    context = {'object': mapping, 'patients': patients, 'doctors': doctors}
    return render(request, 'mappings/mapping_form.html', context)


@login_required(login_url='login')
def mapping_delete_view(request, pk):
    """Delete mapping"""
    mapping = get_object_or_404(PatientDoctorMapping, pk=pk, patient__created_by=request.user)
    
    if request.method == 'POST':
        mapping.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('mapping-list')
    
    return render(request, 'mappings/mapping_confirm_delete.html', {'object': mapping})


# Auth Views
def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password')
            return render(request, 'authentication/login.html')
        
        from django.contrib.auth import authenticate, login
        # Authenticate using custom backend
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'authentication/login.html')


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validation
        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'authentication/register.html')
        
        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'authentication/register.html')
        
        if not password or not password_confirm:
            messages.error(request, 'Password is required')
            return render(request, 'authentication/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/register.html', {
                'name': name,
                'email': email,
            })
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'authentication/register.html', {
                'name': name,
                'email': email,
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered. Please try logging in.')
            return render(request, 'authentication/register.html', {
                'name': name,
            })
        
        try:
            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
                name=name
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'authentication/register.html')


def logout_view(request):
    """User logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    """User profile"""
    context = {
        'user': request.user,
        'total_patients': Patient.objects.filter(created_by=request.user).count(),
        'total_doctors': Doctor.objects.filter(created_by=request.user).count(),
        'total_mappings': PatientDoctorMapping.objects.filter(patient__created_by=request.user).count(),
    }
    return render(request, 'authentication/profile.html', context)


@login_required(login_url='login')
def settings_view(request):
    """User settings"""
    if request.method == 'POST':
        try:
            # Update general settings
            if 'name' in request.POST and 'email' in request.POST:
                request.user.name = request.POST.get('name', request.user.name)
                email = request.POST.get('email', request.user.email)
                
                # Check if email is already in use
                if email != request.user.email and User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already in use.')
                else:
                    request.user.email = email
                    request.user.save()
                    messages.success(request, 'General settings updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating settings: {str(e)}')
    
    context = {
        'user': request.user,
    }
    return render(request, 'authentication/settings.html', context)
