from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.contrib import messages
from .models import User, LoginHistory
from .forms import UserCreationForm, UserUpdateForm
from .mixins import AdminRequiredMixin
from apps.applications.models import Application
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
            context['total_clients'] = Client.objects.count()
            context['total_applications'] = Application.objects.count()
            context['new_applications'] = Application.objects.filter(status__code='new').count()
            context['total_operators'] = User.objects.filter(role='operator').count()
        else:
            context['my_applications'] = Application.objects.filter(operator=user)
            context['pending_applications'] = context['my_applications'].exclude(
                status__code__in=['success', 'fail']
            ).count()

        return context


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Пользователь успешно создан')
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно обновлен')
        return super().form_valid(form)