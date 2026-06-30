from rest_framework.routers import DefaultRouter

from lessons.viewsets import ModuleViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = router.urls
