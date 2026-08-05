import logging
import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('hope_academy')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        details = response.data if settings.DEBUG else None
        error_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': _extract_message(response.data),
            },
        }
        if details is not None:
            error_data['error']['details'] = details
        response.data = error_data
        logger.warning(
            'API error %s: %s',
            response.status_code,
            error_data['error']['message'],
            extra={'view': context.get('view')},
        )
        return response

    logger.error(
        'Unhandled exception: %s\n%s',
        exc,
        traceback.format_exc(),
        extra={'view': context.get('view')},
    )
    return Response(
        {
            'success': False,
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred.',
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _extract_message(data):
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        for key, value in data.items():
            if isinstance(value, list) and value:
                return f'{key}: {value[0]}'
            return f'{key}: {value}'
    if isinstance(data, list) and data:
        return str(data[0])
    return str(data)
