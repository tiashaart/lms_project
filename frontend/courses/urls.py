from rest_framework.routers import DefaultRouter

from courses.viewsets import CategoryViewSet, CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = router.urls
