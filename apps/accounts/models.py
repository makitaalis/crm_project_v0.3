from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('operator', 'Оператор'),
    ]

    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='operator')
    is_blocked = models.BooleanField('Заблокирован', default=False)
    last_activity = models.DateTimeField('Последняя активность', auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_users')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_admin(self):
        return self.role == 'admin'

    def is_operator(self):
        return self.role == 'operator'


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'История входов'
        verbose_name_plural = 'История входов'
        ordering = ['-timestamp']