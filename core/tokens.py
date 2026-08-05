import logging

from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

logger = logging.getLogger('hope_academy')


def blacklist_user_tokens(user):
    """Blacklist all outstanding refresh tokens for a user."""
    tokens = OutstandingToken.objects.filter(user=user)
    count = 0
    for token in tokens:
        _, created = BlacklistedToken.objects.get_or_create(token=token)
        if created:
            count += 1
    logger.info('Blacklisted %s tokens for user %s', count, user.id)
    return count
