from django.urls import path

from .views import (
    MarkAllNotificationsReadView,
    MarkNotificationReadView,
    NotificationDetailView,
    NotificationListView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
    path('read-all/', MarkAllNotificationsReadView.as_view(), name='notification-read-all'),
]
