import sqlite3
import os

# Проверяем оба возможных пути к базе
paths = ['db.sqlite3', '../db.sqlite3']

for p in paths:
    full_path = os.path.abspath(p)
    if os.path.exists(p):
        print(f"\n🔎 Проверка файла: {p}")
        print(f"📍 Полный путь: {full_path}")
        try:
            conn = sqlite3.connect(p)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cur.fetchall()]
            if tables:
                print(f"✅ Найдены таблицы ({len(tables)} шт):")
                print(", ".join(tables[:10]) + "...")
                
                if 'auth_user' in tables:
                    cur.execute("SELECT id, username FROM auth_user;")
                    users = cur.fetchall()
                    print(f"👤 Пользователи в этой базе: {users}")
            else:
                print("⚠️ База пустая (таблиц нет).")
            conn.close()
        except Exception as e:
            print(f"❌ Ошибка при чтении: {e}")
    else:
        print(f"\n❌ Файл {p} не найден по пути {full_path}")