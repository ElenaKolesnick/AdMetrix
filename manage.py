import os
import sys

def main():
    # Указываем на папку dashboard, которая теперь в корне
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    
    # Добавляем корень проекта в пути поиска, чтобы папка 'app' была видна
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Ошибка импорта Django") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()