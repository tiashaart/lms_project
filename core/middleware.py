import logging

audit_logger = logging.getLogger('hope_academy.audit')


class ExceptionHandlingMiddleware:
    """Catch unhandled exceptions outside DRF views."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        from django.http import JsonResponse
        import logging
        logger = logging.getLogger('hope_academy')
        if request.path.startswith('/api/'):
            logger.error('Middleware caught: %s', exception, exc_info=True)
            return JsonResponse(
                {
                    'success': False,
                    'error': {
                        'code': 500,
                        'message': 'An unexpected error occurred.',
                    },
                },
                status=500,
            )
        return None


class AuditLogMiddleware:
    """Log authenticated API mutations for audit trail."""

    AUDIT_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.path.startswith('/api/')
            and request.method in self.AUDIT_METHODS
            and hasattr(request, 'user')
            and request.user.is_authenticated
        ):
            audit_logger.info(
                'user=%s method=%s path=%s status=%s ip=%s',
                request.user.id,
                request.method,
                request.path,
                response.status_code,
                self._get_client_ip(request),
            )
        return response

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
