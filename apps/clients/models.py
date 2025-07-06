from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Client(models.Model):
    name = models.CharField('ФИО', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, db_index=True)
    email = models.EmailField('Email', blank=True)
    address = models.TextField('Адрес', blank=True)
    source = models.CharField('Источник', max_length=100, blank=True)
    notes = models.TextField('Примечания', blank=True)

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_clients')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name or self.phone or f'Клиент #{self.pk}'


class ClientHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField('Поле', max_length=50)
    old_value = models.TextField('Старое значение', blank=True)
    new_value = models.TextField('Новое значение', blank=True)
    timestamp = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        verbose_name = 'История изменений'
        verbose_name_plural = 'История изменений'
        ordering = ['-timestamp']