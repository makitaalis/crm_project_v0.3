from .models import Application, ApplicationHistory, ApplicationComment, Status
from apps.accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from .models import Application, ApplicationHistory, ApplicationComment
from .forms import ApplicationForm, ApplicationOperatorForm
from apps.accounts.mixins import AdminRequiredMixin


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/application_list.html'
    context_object_name = 'applications'
    paginate_by = 20

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
            queryset = queryset.filter(operator_id=operator)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        if self.request.user.is_admin():
            context['operators'] = User.objects.filter(role='operator')
        return context


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'applications/application_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_operator():
            queryset = queryset.filter(operator=self.request.user)
        return queryset


class ApplicationAssignView(AdminRequiredMixin, UpdateView):
    model = Application
    fields = ['operator']
    template_name = 'applications/application_assign.html'

    def form_valid(self, form):
        old_operator = self.object.operator
        response = super().form_valid(form)

        # Log action
        ApplicationHistory.objects.create(
            application=self.object,
            user=self.request.user,
            action=f'Назначен оператор: {self.object.operator}'
        )

        messages.success(self.request, 'Заявка успешно назначена')
        return response

    def get_success_url(self):
        return reverse_lazy('applications:detail', kwargs={'pk': self.object.pk})


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Application
    template_name = 'applications/application_update.html'

    def get_form_class(self):
        if self.request.user.is_admin():
            return ApplicationForm
        return ApplicationOperatorForm

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_operator():
            queryset = queryset.filter(operator=self.request.user)
        return queryset

    def form_valid(self, form):
        old_status = self.object.status
        response = super().form_valid(form)

        # Log status change
        if 'status' in form.changed_data:
            ApplicationHistory.objects.create(
                application=self.object,
                user=self.request.user,
                action=f'Изменен статус: {old_status} → {self.object.status}',
                comment=form.cleaned_data.get('status_comment', '')
            )

        messages.success(self.request, 'Заявка успешно обновлена')
        return response

    def get_success_url(self):
        if self.request.user.is_operator():
            return reverse_lazy('applications:list')
        return reverse_lazy('applications:detail', kwargs={'pk': self.object.pk})