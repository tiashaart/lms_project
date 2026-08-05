from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'Hope Academy LMS API',
        'version': '1.0.0',
    })


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('', include('users.urls')),
    path('', include('courses.urls')),
    path('', include('lessons.urls')),
    path('', include('quizzes.urls')),
    path('', include('assignments.urls')),
    path('', include('progress.urls')),
    path('', include('certificates.urls')),
    path('', include('payments.urls')),
    path('', include('announcements.urls')),
    path('reports/', include('reports.urls')),
]
