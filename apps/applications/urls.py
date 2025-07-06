from django.urls import path
from .views import (
    ApplicationListView, ApplicationDetailView, ApplicationAssignView,
    ApplicationUpdateView, ApplicationCreateView,
    StatusListView, StatusCreateView, StatusUpdateView,
    CategoryListView, CategoryCreateView, CategoryUpdateView
)

app_name = 'applications'

urlpatterns = [
    # Заявки
    path('', ApplicationListView.as_view(), name='list'),
    path('create/', ApplicationCreateView.as_view(), name='create'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='detail'),
    path('<int:pk>/assign/', ApplicationAssignView.as_view(), name='assign'),
    path('<int:pk>/update/', ApplicationUpdateView.as_view(), name='update'),

    # Статусы
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/create/', StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/edit/', StatusUpdateView.as_view(), name='status_edit'),

    # Категории
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),

    path('export/', ExportApplicationsView.as_view(), name='export'),
]