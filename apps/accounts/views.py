from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, View
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import User, LoginHistory
from .forms import UserCreationForm, UserUpdateForm
from .mixins import AdminRequiredMixin
from apps.applications.models import Application, Status
from apps.clients.models import Client


class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Log IP address
        user = form.get_user()
        LoginHistory.objects.create(
            user=user,
            ip_address=self.request.META.get('REMOTE_ADDR', '0.0.0.0'),
            success=True
        )
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_admin():
            # Статистика для админа
            context['total_clients'] = Client.objects.count()
            context['total_applications'] = Application.objects.count()
            context['new_applications'] = Application.objects.filter(status__code='new').count()
            context['total_operators'] = User.objects.filter(role='operator').count()

            # Операторы онлайн (были активны последние 5 минут)
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            context['online_operators'] = User.objects.filter(
                role='operator',
                last_activity__gte=five_minutes_ago
            ).count()

            # Заявки без оператора
            context['unassigned_applications'] = Application.objects.filter(
                operator__isnull=True,
                status__code='new'
            ).count()

        else:
            # Для оператора
            context['my_applications'] = Application.objects.filter(operator=user)
            context['pending_applications'] = context['my_applications'].exclude(
                status__code__in=['success', 'fail']
            ).count()

            # Заявки на перезвон
            context['recall_applications'] = context['my_applications'].filter(
                status__code='recall',
                recall_date__lte=timezone.now()
            ).count()

            # Обработано сегодня
            today = timezone.now().date()
            context['today_processed'] = context['my_applications'].filter(
                updated_at__date=today,
                status__code__in=['success', 'fail']
            ).count()

        return context


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_operator():
            queryset = queryset.filter(operator=user)

        # Filters
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status__code=status)

        operator = self.request.GET.get('operator')
        if operator and user.is_admin():
            if operator == 'none':
                queryset = queryset.filter(operator__isnull=True)
            else:
                queryset = queryset.filter(operator_id=operator)

        return queryset.select_related('client', 'operator', 'status')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        five_minutes_ago = timezone.now() - timedelta(minutes=5)

        # Добавляем информацию об онлайн статусе
        for user in context['users']:
            user.is_online = user.last_activity >= five_minutes_ago
            # Статистика по заявкам
            user.active_applications = user.applications.exclude(
                status__code__in=['success', 'fail']
            ).count()
            user.total_applications = user.applications.count()

        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Пользователь {form.instance.username} успешно создан. Пароль: установлен')
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно обновлен')
        return super().form_valid(form)


class UserBlockView(AdminRequiredMixin, View):
    """Блокировка/разблокировка пользователя"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:  # Нельзя заблокировать себя
            user.is_blocked = not user.is_blocked
            user.save()

            action = "заблокирован" if user.is_blocked else "разблокирован"
            messages.success(request, f'Пользователь {user.username} {action}')
        else:
            messages.error(request, 'Вы не можете заблокировать себя')

        return redirect('accounts:user_list')


class UserPasswordResetView(AdminRequiredMixin, View):
    """Сброс пароля пользователя"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        new_password = User.objects.make_random_password(length=8)
        user.set_password(new_password)
        user.save()

        messages.success(
            request,
            f'Пароль для {user.username} сброшен. Новый пароль: {new_password}'
        )
        return redirect('accounts:user_list')