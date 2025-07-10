from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib import messages


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Проверяем, не заблокирован ли пользователь
            if request.user.is_blocked:
                messages.error(request, 'Ваш аккаунт был заблокирован')
                logout(request)
                return redirect('accounts:login')

            # Проверяем время последней активности
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity > timedelta(hours=12):
                    messages.info(request, 'Сессия истекла. Войдите снова.')
                    logout(request)
                    return redirect('accounts:login')

            # Обновляем время активности
            request.session['last_activity'] = timezone.now().isoformat()

            # Обновляем время активности в модели пользователя
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])

        response = self.get_response(request)
        return response