from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Patient
from .serializers import (
    PatientSerializer,
    PatientListSerializer,
    PatientUpdateSerializer
)
from authentication.utils import success_response, error_response


class PatientPagination(PageNumberPagination):
    """Custom pagination for patient list."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PatientListCreateView(APIView):
    """
    API endpoint for listing and creating patients.
    GET: Retrieve all patients created by authenticated user.
    POST: Create a new patient.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = PatientPagination
    
    def get(self, request):
        """
        Retrieve all patients created by the authenticated user.
        Supports filtering, search, and pagination.
        
        Query Parameters:
        - search: Search by name, phone, or email
        - gender: Filter by gender (M/F/O)
        - city: Filter by city
        - is_active: Filter by active status (true/false)
        - page: Page number
        - page_size: Number of items per page
        """
        try:
            # Get patients for the authenticated user
            queryset = Patient.objects.filter(created_by=request.user)
            
            # Apply filters
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                is_active_bool = is_active.lower() == 'true'
                queryset = queryset.filter(is_active=is_active_bool)
            
            gender = request.query_params.get('gender')
            if gender:
                queryset = queryset.filter(gender=gender.upper())
            
            city = request.query_params.get('city')
            if city:
                queryset = queryset.filter(city__icontains=city)
            
            # Apply search
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(phone__icontains=search) |
                    Q(email__icontains=search)
                )
            
            # Pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            
            # Serialize data
            serializer = PatientListSerializer(paginated_queryset, many=True)
            
            # Return paginated response
            return paginator.get_paginated_response({
                'success': True,
                'message': 'Patients retrieved successfully',
                'data': serializer.data
            })
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving patients",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Create a new patient.
        
        Request body: All patient fields as defined in PatientSerializer
        """
        try:
            serializer = PatientSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                patient = serializer.save()
                
                return success_response(
                    data=PatientSerializer(patient).data,
                    message="Patient created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while creating patient",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific patient.
    GET: Retrieve patient details.
    PUT: Update patient details.
    DELETE: Delete patient record.
    """
    permission_classes = [IsAuthenticated]
    
    def get_patient(self, patient_id, user):
        """Helper method to get patient and verify ownership."""
        try:
            return Patient.objects.get(id=patient_id, created_by=user)
        except Patient.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """
        Get details of a specific patient.
        """
        try:
            patient = self.get_patient(pk, request.user)
            
            if not patient:
                return error_response(
                    message="Patient not found",
                    details="Patient does not exist or you don't have permission to access it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientSerializer(patient)
            
            return success_response(
                data=serializer.data,
                message="Patient details retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving patient details",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        """
        Update patient details.
        
        Request body: Patient fields to update
        """
        try:
            patient = self.get_patient(pk, request.user)
            
            if not patient:
                return error_response(
                    message="Patient not found",
                    details="Patient does not exist or you don't have permission to update it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientUpdateSerializer(
                patient,
                data=request.data,
                partial=False  # Require all fields for PUT
            )
            
            if serializer.is_valid():
                updated_patient = serializer.save()
                
                return success_response(
                    data=PatientSerializer(updated_patient).data,
                    message="Patient updated successfully",
                    status_code=status.HTTP_200_OK
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while updating patient",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, pk):
        """
        Partially update patient details.
        
        Request body: Patient fields to update (partial)
        """
        try:
            patient = self.get_patient(pk, request.user)
            
            if not patient:
                return error_response(
                    message="Patient not found",
                    details="Patient does not exist or you don't have permission to update it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientUpdateSerializer(
                patient,
                data=request.data,
                partial=True  # Allow partial updates for PATCH
            )
            
            if serializer.is_valid():
                updated_patient = serializer.save()
                
                return success_response(
                    data=PatientSerializer(updated_patient).data,
                    message="Patient updated successfully",
                    status_code=status.HTTP_200_OK
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while updating patient",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        """
        Delete a patient record.
        """
        try:
            patient = self.get_patient(pk, request.user)
            
            if not patient:
                return error_response(
                    message="Patient not found",
                    details="Patient does not exist or you don't have permission to delete it",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            patient_data = {
                'id': patient.id,
                'full_name': patient.full_name,
                'phone': patient.phone
            }
            
            patient.delete()
            
            return success_response(
                data=patient_data,
                message="Patient deleted successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while deleting patient",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )