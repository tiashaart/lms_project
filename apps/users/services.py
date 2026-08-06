import logging
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import connection

from core.tokens import blacklist_user_tokens
from .models import EmailVerificationToken, PasswordResetToken


def link_user(django_user_id, supabase_uuid):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO public.user_auth_map (django_user_id, auth_user_id)
            VALUES (%s, %s)
            ON CONFLICT (django_user_id) DO UPDATE
            SET auth_user_id = EXCLUDED.auth_user_id;
            """,
            (django_user_id, supabase_uuid),
        )


User = get_user_model()
logger = logging.getLogger("hope_academy")


class AuthService:
    @staticmethod
    def _send_email(subject, message, recipient_list):
        try:
            from .tasks import send_email_task
            send_email_task.delay(subject, message, recipient_list)
        except Exception:
            from django.core.mail import send_mail
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

    @staticmethod
    def create_user(validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        AuthService.send_verification_email(user)
        return user

    @staticmethod
    def send_verification_email(user):
        EmailVerificationToken.objects.filter(user=user, is_used=False).update(is_used=True)
        token = EmailVerificationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=24),
        )
        verify_url = f'{settings.FRONTEND_URL}/verify-email/{token.token}'
        AuthService._send_email(
            subject='Verify your Hope Academy account',
            message=f'Click to verify your email: {verify_url}',
            recipient_list=[user.email],
        )
        logger.info('Verification email queued for user %s', user.id)

    @staticmethod
    def resend_verification(user):
        if user.email_verified:
            return False, 'Email is already verified.'
        AuthService.send_verification_email(user)
        return True, 'Verification email sent.'

    @staticmethod
    def verify_email(token_str):
        try:
            token_uuid = uuid.UUID(str(token_str))
        except ValueError:
            return False, 'Invalid verification token.'

        token = EmailVerificationToken.objects.filter(
            token=token_uuid, is_used=False, expires_at__gt=timezone.now(),
        ).select_related('user').first()

        if not token:
            return False, 'Token is invalid or expired.'

        user = token.user
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        token.is_used = True
        token.save(update_fields=['is_used'])
        return True, 'Email verified successfully.'

    @staticmethod
    def request_password_reset(email):
        user = User.objects.filter(email=email).first()
        if not user:
            return True

        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=1),
        )
        reset_url = f'{settings.FRONTEND_URL}/reset-password/{token.token}'
        AuthService._send_email(
            subject='Reset your Hope Academy password',
            message=f'Click to reset your password: {reset_url}',
            recipient_list=[user.email],
        )
        logger.info('Password reset email queued for user %s', user.id)
        return True

    @staticmethod
    def reset_password(token_str, new_password):
        try:
            token_uuid = uuid.UUID(str(token_str))
        except ValueError:
            return False, 'Invalid reset token.'

        token = PasswordResetToken.objects.filter(
            token=token_uuid, is_used=False, expires_at__gt=timezone.now(),
        ).select_related('user').first()

        if not token:
            return False, 'Token is invalid or expired.'

        user = token.user
        user.set_password(new_password)
        user.save()
        token.is_used = True
        token.save(update_fields=['is_used'])
        blacklist_user_tokens(user)
        return True, 'Password reset successfully.'

    @staticmethod
    def change_password(user, old_password, new_password):
        if not user.check_password(old_password):
            return False, 'Current password is incorrect.'
        user.set_password(new_password)
        user.save()
        blacklist_user_tokens(user)
        return True, 'Password changed successfully.'

    @staticmethod
    def logout_all(user):
        blacklist_user_tokens(user)
        return True, 'All sessions have been logged out.'

