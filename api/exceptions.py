from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """Custom API exception handler with consistent error format."""
    response = exception_handler(exc, context)

    if response is not None:
        error_payload = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': _get_error_message(response.data),
                'details': response.data,
            },
        }
        response.data = error_payload

    return response


def _get_error_message(data):
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        for key, value in data.items():
            if isinstance(value, list):
                return f'{key}: {value[0]}'
            return str(value)
    if isinstance(data, list):
        return str(data[0])
    return 'An error occurred.'
