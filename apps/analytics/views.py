from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'