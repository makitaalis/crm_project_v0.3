def notifications(request):
    """Контекстный процессор для уведомлений"""
    context = {}

    if request.user.is_authenticated:
        if request.user.is_admin():
            # Для админа
            from apps.applications.models import Application
            from apps.accounts.models import User
            from django.utils import timezone
            from datetime import timedelta

            # Неназначенные заявки
            context['unassigned_count'] = Application.objects.filter(
                operator__isnull=True
            ).count()

            # Просроченные заявки
            context['overdue_count'] = Application.objects.filter(
                created_at__lt=timezone.now() - timedelta(days=1),
                status__is_final=False
            ).count()

        elif request.user.is_operator():
            # Для оператора
            from apps.applications.models import Application
            from django.utils import timezone

            # Мои активные заявки
            context['my_active_count'] = Application.objects.filter(
                operator=request.user,
                status__is_final=False
            ).count()

            # Заявки на перезвон
            context['recall_count'] = Application.objects.filter(
                operator=request.user,
                status__code='recall',
                recall_date__lte=timezone.now()
            ).count()

    return context