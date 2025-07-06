from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView, UserListView, UserCreateView, UserUpdateView,
    UserBlockView, UserPasswordResetView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/block/', UserBlockView.as_view(), name='user_block'),
    path('users/<int:pk>/reset-password/', UserPasswordResetView.as_view(), name='user_reset_password'),
]