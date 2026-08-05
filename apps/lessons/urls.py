from django.urls import path

from .views import (
    ModuleViewSet,
    LessonViewSet,
    ModuleReorderView,
    LessonReorderView,
)


urlpatterns = [

    # Modules list + create
    path(
        "courses/<int:course_pk>/modules/",
        ModuleViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="module-list-create",
    ),


    # Lessons list + create
    path(
        "courses/<int:course_pk>/modules/<int:module_pk>/lessons/",
        LessonViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="lesson-list-create",
    ),


    # Reorder modules
    path(
        "courses/<int:course_pk>/modules/reorder/",
        ModuleReorderView.as_view(),
        name="module-reorder",
    ),


    # Reorder lessons
    path(
        "courses/<int:course_pk>/modules/<int:module_pk>/lessons/reorder/",
        LessonReorderView.as_view(),
        name="lesson-reorder",
    ),

]