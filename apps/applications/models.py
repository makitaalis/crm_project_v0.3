from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.clients.models import Client

User = get_user_model()


class Status(models.Model):
    code = models.CharField('Код', max_length=50, unique=True)
    name = models.CharField('Название', max_length=100)
    color = models.CharField('Цвет', max_length=7, default='#6c757d')
    is_final = models.BooleanField('Финальный статус', default=False)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['order']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    color = models.CharField('Цвет', max_length=7, default='#6c757d')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='applications')
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='applications')
    categories = models.ManyToManyField(Category, blank=True, related_name='applications')

    notes = models.TextField('Примечания', blank=True)
    recall_date = models.DateTimeField('Дата перезвона', null=True, blank=True)

    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_applications')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.pk} - {self.client}'

    def is_overdue(self):
        return (timezone.now() - self.created_at).days > 1


class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField('Действие', max_length=200)
    comment = models.TextField('Комментарий', blank=True)
    timestamp = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        verbose_name = 'История заявки'
        verbose_name_plural = 'История заявок'
        ordering = ['-timestamp']


class ApplicationComment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст')
    timestamp = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['timestamp']