from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав администратора"""

    def test_func(self):
        return (self.request.user.is_authenticated and
                self.request.user.is_admin() and
                not self.request.user.is_blocked)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')

        if self.request.user.is_blocked:
            messages.error(self.request, 'Ваш аккаунт заблокирован')
            return redirect('accounts:logout')

        messages.error(self.request, 'У вас нет прав для доступа к этой странице')
        return redirect('dashboard')


class OperatorRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав оператора"""

    def test_func(self):
        return (self.request.user.is_authenticated and
                self.request.user.is_operator() and
                not self.request.user.is_blocked)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')

        if self.request.user.is_blocked:
            messages.error(self.request, 'Ваш аккаунт заблокирован')
            return redirect('accounts:logout')

        messages.error(self.request, 'У вас нет прав для доступа к этой странице')
        return redirect('dashboard')


class AdminOrOperatorMixin(UserPassesTestMixin):
    """Миксин для админов или операторов"""

    def test_func(self):
        return (self.request.user.is_authenticated and
                (self.request.user.is_admin() or self.request.user.is_operator()) and
                not self.request.user.is_blocked)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')

        if self.request.user.is_blocked:
            messages.error(self.request, 'Ваш аккаунт заблокирован')
            return redirect('accounts:logout')

        messages.error(self.request, 'У вас нет прав для доступа к этой странице')
        return redirect('dashboard')