from django.contrib.auth.models import AnonymousUser

from . import mock_data


class DemoUserMiddleware:
    """Attach a demo user to request based on session role."""

    PUBLIC_PATHS = (
        '/', '/login/', '/register/', '/forgot-password/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        role = request.GET.get('role') or request.session.get('demo_role', 'student')

        if request.path.startswith('/logout'):
            request.session.pop('demo_role', None)
            request.demo_user = mock_data.ANONYMOUS_USER
        elif request.path in self.PUBLIC_PATHS or request.path.startswith('/reset-password'):
            if request.session.get('demo_role'):
                request.demo_user = mock_data.get_user(request.session['demo_role'])
            else:
                request.demo_user = mock_data.ANONYMOUS_USER
        else:
            if 'role' in request.GET:
                request.session['demo_role'] = role
            request.demo_user = mock_data.get_user(request.session.get('demo_role', role))

        request.user = request.demo_user
        if not isinstance(request.user, AnonymousUser) and hasattr(request.user, 'is_authenticated'):
            pass
        return self.get_response(request)
