from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all error responses consistently.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'message': 'An error occurred',
                'details': {}
            }
        }
        
        # Handle validation errors
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['message'] = response.data['detail']
            else:
                custom_response_data['error']['message'] = 'Validation error'
                custom_response_data['error']['details'] = response.data
        elif isinstance(response.data, list):
            custom_response_data['error']['message'] = response.data[0] if response.data else 'An error occurred'
        
        response.data = custom_response_data
    
    return response


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Helper function to create consistent success responses.
    """
    response_data = {
        'success': True,
        'message': message,
    }
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message="An error occurred", details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Helper function to create consistent error responses.
    """
    response_data = {
        'success': False,
        'error': {
            'message': message,
        }
    }
    
    if details:
        response_data['error']['details'] = details
    
    return Response(response_data, status=status_code)