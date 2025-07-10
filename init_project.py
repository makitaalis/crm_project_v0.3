"""
Скрипт для инициализации CRM проекта
Запускать после миграций: python init_project.py
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command


def main():
    print("=" * 60)
    print("Инициализация CRM системы")
    print("=" * 60)

    try:
        # Создаем суперпользователя
        print("\n1. Создание суперпользователя...")
        call_command('create_superuser')

        # Создаем начальные данные
        print("\n2. Создание начальных данных...")
        call_command('setup_initial_data')

        print("\n" + "=" * 60)
        print("ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        print("\nТеперь вы можете:")
        print("1. Запустить сервер: python manage.py runserver")
        print("2. Открыть http://127.0.0.1:8000/")
        print("3. Войти под admin/admin123")
        print("\nУдачной работы!")

    except Exception as e:
        print(f"\nОшибка при инициализации: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()