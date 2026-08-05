from django.urls import path

from .views import AnnouncementDetailView, AnnouncementListCreateView, PublishAnnouncementView

urlpatterns = [
    path('', AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('<int:pk>/publish/', PublishAnnouncementView.as_view(), name='announcement-publish'),
]
