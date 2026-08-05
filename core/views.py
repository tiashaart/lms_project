from django.conf import settings
from django.db import connection
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=['System'], summary='Health check')
    def get(self, request):
        db_ok = False
        try:
            connection.ensure_connection()
            db_ok = True
        except Exception:
            pass

        redis_ok = None
        if getattr(settings, 'CELERY_BROKER_URL', None):
            try:
                import redis
                client = redis.from_url(settings.CELERY_BROKER_URL)
                client.ping()
                redis_ok = True
            except Exception:
                redis_ok = False

        status = 'healthy' if db_ok else 'unhealthy'
        return Response({
            'success': db_ok,
            'status': status,
            'checks': {
                'database': db_ok,
                'redis': redis_ok,
            },
        }, status=200 if db_ok else 503)
