from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity > timedelta(hours=12):
                    logout(request)
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response