import sqlite3
import os

# Теперь база лежит в той же папке, что и этот скрипт
db_path = 'db.sqlite3'

print(f"🛠 Проверка базы данных по пути: {os.path.abspath(db_path)}")

if not os.path.exists(db_path):
    print(f"❌ Ошибка: Файл {db_path} не найден в текущей директории!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Начинаю добавление колонок...")
    
    # Добавляем 40 аналитических метрик
    for i in range(1, 41):
        col_name = f'metric_factor_{i:02d}'
        try:
            # REAL — тип данных для чисел с плавающей точкой
            cursor.execute(f"ALTER TABLE app_gamemarketingdata ADD COLUMN {col_name} REAL DEFAULT 0.0")
            print(f"✅ Добавлена: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"⚠️ Уже есть: {col_name}")
            else:
                print(f"❌ Ошибка на {col_name}: {e}")

    conn.commit()
    conn.close()
    print("\n🚀 Готово! База подготовлена к загрузке 50 критериев.")