from django.urls import path

from .profile_views import (
    ProfileChangePasswordView,
    ProfilePictureUploadView,
    ProfileUpdateView,
    ProfileView,
)

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('picture/', ProfilePictureUploadView.as_view(), name='profile-picture'),
    path('change-password/', ProfileChangePasswordView.as_view(), name='profile-change-password'),
]
