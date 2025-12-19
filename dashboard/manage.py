#!/usr/bin/env python
import os
import sys

def main():
    """Точка входа для выполнения административных команд Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен "
            "и виртуальное окружение активировано."
        ) from exc
        
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()