from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.applications.models import Status, Category, Application
from apps.clients.models import Client
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает начальные данные для CRM системы'

    def handle(self, *args, **options):
        self.stdout.write('Создание начальных данных...')

        # Создаем статусы
        self.create_statuses()

        # Создаем админа
        self.create_admin()

        # Создаем операторов
        self.create_operators()

        # Создаем категории
        self.create_categories()

        # Создаем тестовых клиентов
        self.create_clients()

        # Создаем тестовые заявки
        self.create_applications()

        self.stdout.write(
            self.style.SUCCESS('Начальные данные успешно созданы!')
        )

        # Показываем данные для входа
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('ДАННЫЕ ДЛЯ ВХОДА В СИСТЕМУ:')
        self.stdout.write('=' * 50)
        self.stdout.write('Администратор:')
        self.stdout.write('  Логин: admin')
        self.stdout.write('  Пароль: admin123')
        self.stdout.write('')
        self.stdout.write('Операторы:')
        self.stdout.write('  operator1 / operator123')
        self.stdout.write('  operator2 / operator123')
        self.stdout.write('  operator3 / operator123')
        self.stdout.write('=' * 50)

    def create_statuses(self):
        """Создание статусов заявок"""
        statuses = [
            {'code': 'new', 'name': 'Новая', 'color': '#1f6feb', 'order': 1},
            {'code': 'in_work', 'name': 'В работе', 'color': '#f78166', 'order': 2},
            {'code': 'recall', 'name': 'Перезвонить', 'color': '#a371f7', 'order': 3},
            {'code': 'success', 'name': 'Успешно', 'color': '#238636', 'is_final': True, 'order': 4},
            {'code': 'fail', 'name': 'Отказ', 'color': '#da3633', 'is_final': True, 'order': 5},
        ]

        for status_data in statuses:
            status, created = Status.objects.get_or_create(
                code=status_data['code'],
                defaults=status_data
            )
            if created:
                self.stdout.write(f'Создан статус: {status.name}')

    def create_admin(self):
        """Создание администратора"""
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                password='admin123',
                first_name='Администратор',
                last_name='Системы',
                email='admin@crm.local',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'Создан администратор: {admin.username}')

    def create_operators(self):
        """Создание операторов"""
        operators_data = [
            {'username': 'operator1', 'first_name': 'Иван', 'last_name': 'Петров'},
            {'username': 'operator2', 'first_name': 'Мария', 'last_name': 'Сидорова'},
            {'username': 'operator3', 'first_name': 'Алексей', 'last_name': 'Козлов'},
        ]

        admin = User.objects.get(username='admin')

        for op_data in operators_data:
            if not User.objects.filter(username=op_data['username']).exists():
                operator = User.objects.create_user(
                    username=op_data['username'],
                    password='operator123',
                    first_name=op_data['first_name'],
                    last_name=op_data['last_name'],
                    email=f"{op_data['username']}@crm.local",
                    role='operator',
                    created_by=admin
                )
                self.stdout.write(f'Создан оператор: {operator.username}')

    def create_categories(self):
        """Создание категорий"""
        categories = [
            {'name': 'Горячий лид', 'color': '#da3633'},
            {'name': 'Холодный лид', 'color': '#1f6feb'},
            {'name': 'Повторное обращение', 'color': '#238636'},
            {'name': 'VIP клиент', 'color': '#a371f7'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

    def create_clients(self):
        """Создание тестовых клиентов"""
        clients_data = [
            {'name': 'Иван Иванов', 'phone': '9991234567', 'email': 'ivan@test.ru', 'source': 'Сайт'},
            {'name': 'Петр Петров', 'phone': '9992345678', 'email': 'petr@test.ru', 'source': 'Реклама'},
            {'name': 'Мария Сидорова', 'phone': '9993456789', 'email': 'maria@test.ru', 'source': 'Рекомендация'},
            {'name': 'Анна Козлова', 'phone': '9994567890', 'email': 'anna@test.ru', 'source': 'Социальные сети'},
            {'name': 'Сергей Смирнов', 'phone': '9995678901', 'email': 'sergey@test.ru',
             'source': 'Контекстная реклама'},
        ]

        admin = User.objects.get(username='admin')

        for client_data in clients_data:
            if not Client.objects.filter(phone=client_data['phone']).exists():
                client = Client.objects.create(
                    **client_data,
                    address=f"г. Москва, ул. Тестовая, д. {random.randint(1, 100)}",
                    notes=f"Тестовый клиент для демонстрации системы",
                    created_by=admin
                )
                self.stdout.write(f'Создан клиент: {client.name}')

    def create_applications(self):
        """Создание тестовых заявок"""
        clients = list(Client.objects.all())
        operators = list(User.objects.filter(role='operator'))
        statuses = list(Status.objects.all())
        categories = list(Category.objects.all())
        admin = User.objects.get(username='admin')

        # Создаем разные типы заявок
        applications_to_create = [
            # Новые заявки без оператора
            {'client': clients[0], 'operator': None, 'status': Status.objects.get(code='new')},
            {'client': clients[1], 'operator': None, 'status': Status.objects.get(code='new')},

            # Заявки в работе
            {'client': clients[2], 'operator': operators[0], 'status': Status.objects.get(code='in_work')},
            {'client': clients[3], 'operator': operators[1], 'status': Status.objects.get(code='in_work')},

            # Заявки на перезвон
            {'client': clients[4], 'operator': operators[0], 'status': Status.objects.get(code='recall')},

            # Закрытые заявки
            {'client': clients[0], 'operator': operators[2], 'status': Status.objects.get(code='success')},
            {'client': clients[1], 'operator': operators[1], 'status': Status.objects.get(code='fail')},
        ]

        for i, app_data in enumerate(applications_to_create):
            if Application.objects.count() < 10:  # Ограничиваем количество
                app = Application.objects.create(
                    client=app_data['client'],
                    operator=app_data['operator'],
                    status=app_data['status'],
                    notes=f"Тестовая заявка #{i + 1} для демонстрации системы",
                    created_by=admin
                )

                # Добавляем случайные категории
                if categories:
                    selected_categories = random.sample(categories, random.randint(1, 2))
                    app.categories.set(selected_categories)

                self.stdout.write(f'Создана заявка #{app.pk} для {app.client.name}')