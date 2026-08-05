from rest_framework.routers import DefaultRouter

from assignments.viewsets import AssignmentViewSet, AssignmentSubmissionViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')

urlpatterns = router.urls
