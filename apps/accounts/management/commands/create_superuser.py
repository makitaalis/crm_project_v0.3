from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает суперпользователя admin/admin123 если его нет'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@crm.local',
                first_name='Администратор',
                last_name='Системы',
                role='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь {admin.username} создан успешно!')
            )
            self.stdout.write('Логин: admin')
            self.stdout.write('Пароль: admin123')
        else:
            self.stdout.write(
                self.style.WARNING('Суперпользователь admin уже существует')
            )