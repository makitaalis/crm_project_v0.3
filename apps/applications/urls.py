from django.urls import path
from .views import ApplicationListView, ApplicationDetailView, ApplicationAssignView, ApplicationUpdateView

app_name = 'applications'

urlpatterns = [
    path('', ApplicationListView.as_view(), name='list'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='detail'),
    path('<int:pk>/assign/', ApplicationAssignView.as_view(), name='assign'),
    path('<int:pk>/update/', ApplicationUpdateView.as_view(), name='update'),
]