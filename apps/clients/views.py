from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Client
from .forms import ClientForm
from apps.accounts.mixins import AdminRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(phone__icontains=search) |
                models.Q(email__icontains=search)
            )
        return queryset


class ClientCreateView(AdminRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        # Check duplicates
        phone = form.cleaned_data.get('phone')
        if phone and Client.objects.filter(phone=phone).exists():
            messages.warning(self.request, f'Клиент с телефоном {phone} уже существует!')

        messages.success(self.request, 'Клиент успешно добавлен')
        return super().form_valid(form)


class ClientUpdateView(AdminRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        # Log changes
        original = Client.objects.get(pk=self.object.pk)
        for field in form.changed_data:
            ClientHistory.objects.create(
                client=self.object,
                user=self.request.user,
                field_name=field,
                old_value=str(getattr(original, field)),
                new_value=str(getattr(form.instance, field))
            )

        messages.success(self.request, 'Клиент успешно обновлен')
        return super().form_valid(form)


class ClientDeleteView(AdminRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Клиент успешно удален')
        return super().delete(request, *args, **kwargs)