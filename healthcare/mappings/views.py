from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorMappingListSerializer,
    PatientDoctorMappingUpdateSerializer,
    DoctorBasicSerializer
)
from patients.models import Patient
from authentication.utils import success_response, error_response


class MappingPagination(PageNumberPagination):
    """Custom pagination for mapping list."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PatientDoctorMappingListCreateView(APIView):
    """
    API endpoint for listing and creating patient-doctor mappings.
    GET: Retrieve all patient-doctor mappings.
    POST: Create a new mapping (assign doctor to patient).
    """
    permission_classes = [IsAuthenticated]
    pagination_class = MappingPagination
    
    def get(self, request):
        """
        Retrieve all patient-doctor mappings for the authenticated user.
        Supports filtering, search, and pagination.
        
        Query Parameters:
        - patient_id: Filter by patient ID
        - doctor_id: Filter by doctor ID
        - status: Filter by status (ACTIVE/INACTIVE/COMPLETED)
        - search: Search by patient or doctor name
        - page: Page number
        - page_size: Number of items per page
        """
        try:
            # Get mappings where user created the patient
            queryset = PatientDoctorMapping.objects.filter(
                patient__created_by=request.user
            ).select_related('patient', 'doctor', 'created_by')
            
            # Apply filters
            patient_id = request.query_params.get('patient_id')
            if patient_id:
                queryset = queryset.filter(patient_id=patient_id)
            
            doctor_id = request.query_params.get('doctor_id')
            if doctor_id:
                queryset = queryset.filter(doctor_id=doctor_id)
            
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter.upper())
            
            # Apply search
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(patient__first_name__icontains=search) |
                    Q(patient__last_name__icontains=search) |
                    Q(doctor__first_name__icontains=search) |
                    Q(doctor__last_name__icontains=search) |
                    Q(doctor__specialization__icontains=search)
                )
            
            # Pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            
            # Serialize data
            serializer = PatientDoctorMappingListSerializer(paginated_queryset, many=True)
            
            # Return paginated response
            return paginator.get_paginated_response({
                'success': True,
                'message': 'Mappings retrieved successfully',
                'data': serializer.data
            })
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving mappings",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Create a new patient-doctor mapping.
        Assign a doctor to a patient.
        
        Request body:
        {
            "patient": patient_id,
            "doctor": doctor_id,
            "reason": "Medical condition or reason",
            "notes": "Additional notes",
            "status": "ACTIVE" (optional, defaults to ACTIVE)
        }
        """
        try:
            serializer = PatientDoctorMappingSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                mapping = serializer.save()
                
                return success_response(
                    data=PatientDoctorMappingSerializer(mapping).data,
                    message="Doctor assigned to patient successfully",
                    status_code=status.HTTP_201_CREATED
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while creating mapping",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientDoctorsView(APIView):
    """
    API endpoint to get all doctors assigned to a specific patient.
    GET: Retrieve all doctors for a patient.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, patient_id):
        """
        Get all doctors assigned to a specific patient.
        
        Query Parameters:
        - status: Filter by mapping status (ACTIVE/INACTIVE/COMPLETED)
        """
        try:
            # Check if patient exists and belongs to the user
            try:
                patient = Patient.objects.get(
                    id=patient_id,
                    created_by=request.user
                )
            except Patient.DoesNotExist:
                return error_response(
                    message="Patient not found",
                    details="Patient does not exist or you don't have permission to access it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Get all mappings for this patient
            queryset = PatientDoctorMapping.objects.filter(
                patient=patient
            ).select_related('doctor')
            
            # Apply status filter if provided
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter.upper())
            
            # Serialize data
            serializer = PatientDoctorMappingSerializer(queryset, many=True)
            
            response_data = {
                'patient': {
                    'id': patient.id,
                    'full_name': patient.full_name,
                    'age': patient.age,
                    'phone': patient.phone,
                    'email': patient.email
                },
                'doctors_count': queryset.count(),
                'mappings': serializer.data
            }
            
            return success_response(
                data=response_data,
                message=f"Retrieved {queryset.count()} doctor(s) for patient {patient.full_name}",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving patient doctors",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientDoctorMappingDetailView(APIView):
    """
    API endpoint for managing a specific patient-doctor mapping.
    GET: Retrieve mapping details.
    PATCH: Update mapping status/notes.
    DELETE: Remove doctor from patient (delete mapping).
    """
    permission_classes = [IsAuthenticated]
    
    def get_mapping(self, mapping_id, user):
        """Helper method to get mapping and verify ownership."""
        try:
            return PatientDoctorMapping.objects.select_related(
                'patient', 'doctor', 'created_by'
            ).get(
                id=mapping_id,
                patient__created_by=user
            )
        except PatientDoctorMapping.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """
        Get details of a specific mapping.
        """
        try:
            mapping = self.get_mapping(pk, request.user)
            
            if not mapping:
                return error_response(
                    message="Mapping not found",
                    details="Mapping does not exist or you don't have permission to access it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientDoctorMappingSerializer(mapping)
            
            return success_response(
                data=serializer.data,
                message="Mapping details retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving mapping details",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, pk):
        """
        Update mapping status or notes.
        
        Request body:
        {
            "status": "INACTIVE" or "COMPLETED",
            "notes": "Updated notes"
        }
        """
        try:
            mapping = self.get_mapping(pk, request.user)
            
            if not mapping:
                return error_response(
                    message="Mapping not found",
                    details="Mapping does not exist or you don't have permission to update it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientDoctorMappingUpdateSerializer(
                mapping,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                updated_mapping = serializer.save()
                
                return success_response(
                    data=PatientDoctorMappingSerializer(updated_mapping).data,
                    message="Mapping updated successfully",
                    status_code=status.HTTP_200_OK
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while updating mapping",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        """
        Delete a mapping (remove doctor from patient).
        """
        try:
            mapping = self.get_mapping(pk, request.user)
            
            if not mapping:
                return error_response(
                    message="Mapping not found",
                    details="Mapping does not exist or you don't have permission to delete it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            mapping_data = {
                'id': mapping.id,
                'patient_name': mapping.patient.full_name,
                'doctor_name': mapping.doctor.full_name,
                'assigned_date': mapping.assigned_date
            }
            
            mapping.delete()
            
            return success_response(
                data=mapping_data,
                message="Doctor removed from patient successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while deleting mapping",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )