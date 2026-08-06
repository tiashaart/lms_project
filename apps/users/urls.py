from django.urls import path

from .admin_views import AdminUserDetailView, AdminUserListCreateView
from .views import (
    ChangePasswordView,
    EmailVerificationView,
    LoginView,
    LogoutAllView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RefreshTokenView,
    RegisterView,
    ResendVerificationView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('users/', AdminUserListCreateView.as_view(), name='admin-users'),
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]
