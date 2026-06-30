from rest_framework.routers import DefaultRouter

from certificates.viewsets import CertificateViewSet

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet, basename='certificate')

urlpatterns = router.urls
