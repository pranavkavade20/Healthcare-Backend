from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Doctor
from .serializers import (
    DoctorSerializer,
    DoctorListSerializer,
    DoctorUpdateSerializer
)
from authentication.utils import success_response, error_response


class DoctorPagination(PageNumberPagination):
    """Custom pagination for doctor list."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DoctorListCreateView(APIView):
    """
    API endpoint for listing and creating doctors.
    GET: Retrieve all doctors (public access with authentication).
    POST: Create a new doctor (authenticated users only).
    """
    permission_classes = [IsAuthenticated]
    pagination_class = DoctorPagination
    
    def get(self, request):
        """
        Retrieve all doctors.
        Supports filtering, search, and pagination.
        
        Query Parameters:
        - search: Search by name, specialization, city, or qualification
        - specialization: Filter by specialization
        - city: Filter by city
        - is_available: Filter by availability (true/false)
        - is_active: Filter by active status (true/false)
        - min_experience: Minimum years of experience
        - max_fee: Maximum consultation fee
        - page: Page number
        - page_size: Number of items per page
        """
        try:
            # Get all doctors
            queryset = Doctor.objects.all()
            
            # Apply filters
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                is_active_bool = is_active.lower() == 'true'
                queryset = queryset.filter(is_active=is_active_bool)
            
            is_available = request.query_params.get('is_available')
            if is_available is not None:
                is_available_bool = is_available.lower() == 'true'
                queryset = queryset.filter(is_available=is_available_bool)
            
            specialization = request.query_params.get('specialization')
            if specialization:
                queryset = queryset.filter(specialization__iexact=specialization)
            
            city = request.query_params.get('city')
            if city:
                queryset = queryset.filter(city__icontains=city)
            
            min_experience = request.query_params.get('min_experience')
            if min_experience:
                try:
                    queryset = queryset.filter(experience_years__gte=int(min_experience))
                except ValueError:
                    pass
            
            max_fee = request.query_params.get('max_fee')
            if max_fee:
                try:
                    queryset = queryset.filter(consultation_fee__lte=float(max_fee))
                except ValueError:
                    pass
            
            # Apply search
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(specialization__icontains=search) |
                    Q(qualification__icontains=search) |
                    Q(city__icontains=search) |
                    Q(clinic_name__icontains=search)
                )
            
            # Pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            
            # Serialize data
            serializer = DoctorListSerializer(paginated_queryset, many=True)
            
            # Return paginated response
            return paginator.get_paginated_response({
                'success': True,
                'message': 'Doctors retrieved successfully',
                'data': serializer.data
            })
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving doctors",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Create a new doctor.
        
        Request body: All doctor fields as defined in DoctorSerializer
        """
        try:
            serializer = DoctorSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                doctor = serializer.save()
                
                return success_response(
                    data=DoctorSerializer(doctor).data,
                    message="Doctor created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while creating doctor",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DoctorDetailView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific doctor.
    GET: Retrieve doctor details.
    PUT: Update doctor details.
    PATCH: Partially update doctor details.
    DELETE: Delete doctor record.
    """
    permission_classes = [IsAuthenticated]
    
    def get_doctor(self, doctor_id):
        """Helper method to get doctor."""
        try:
            return Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """
        Get details of a specific doctor.
        """
        try:
            doctor = self.get_doctor(pk)
            
            if not doctor:
                return error_response(
                    message="Doctor not found",
                    details="Doctor does not exist",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = DoctorSerializer(doctor)
            
            return success_response(
                data=serializer.data,
                message="Doctor details retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while retrieving doctor details",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        """
        Update doctor details (full update).
        Only the creator can update the doctor.
        
        Request body: All doctor fields to update
        """
        try:
            doctor = self.get_doctor(pk)
            
            if not doctor:
                return error_response(
                    message="Doctor not found",
                    details="Doctor does not exist",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user is the creator
            if doctor.created_by != request.user:
                return error_response(
                    message="Permission denied",
                    details="You don't have permission to update this doctor",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            serializer = DoctorUpdateSerializer(
                doctor,
                data=request.data,
                partial=False,  # Require all fields for PUT
                context={'request': request}
            )
            
            if serializer.is_valid():
                updated_doctor = serializer.save()
                
                return success_response(
                    data=DoctorSerializer(updated_doctor).data,
                    message="Doctor updated successfully",
                    status_code=status.HTTP_200_OK
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while updating doctor",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        """
        Delete a doctor record.
        Only the creator can delete the doctor.
        """
        try:
            doctor = self.get_doctor(pk)
            
            if not doctor:
                return error_response(
                    message="Doctor not found",
                    details="Doctor does not exist",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user is the creator
            if doctor.created_by != request.user:
                return error_response(
                    message="Permission denied",
                    details="You don't have permission to delete this doctor",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            doctor_data = {
                'id': doctor.id,
                'full_name': doctor.full_name,
                'specialization': doctor.get_specialization_display(),
                'license_number': doctor.license_number
            }
            
            doctor.delete()
            
            return success_response(
                data=doctor_data,
                message="Doctor deleted successfully",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while deleting doctor",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, pk):
        """
        Partially update doctor details.
        Only the creator can update the doctor.
        
        Request body: Doctor fields to update (partial)
        """
        try:
            doctor = self.get_doctor(pk)
            
            if not doctor:
                return error_response(
                    message="Doctor not found",
                    details="Doctor does not exist",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user is the creator
            if doctor.created_by != request.user:
                return error_response(
                    message="Permission denied",
                    details="You don't have permission to update this doctor",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            serializer = DoctorUpdateSerializer(
                doctor,
                data=request.data,
                partial=True,  # Allow partial updates for PATCH
                context={'request': request}
            )
            
            if serializer.is_valid():
                updated_doctor = serializer.save()
                
                return success_response(
                    data=DoctorSerializer(updated_doctor).data,
                    message="Doctor updated successfully",
                    status_code=status.HTTP_200_OK
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred while updating doctor",
                details=str(e),
                status_code=status.HTTP_500_)