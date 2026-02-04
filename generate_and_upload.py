import pandas as pd
import sqlite3
import numpy as np
import os
from datetime import datetime, timedelta

# --- НАСТРОЙКА ПУТИ ---
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'db.sqlite3')

def get_table_columns(conn, table_name):
    """Получает список всех колонок из существующей таблицы в БД"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]

if not os.path.exists(db_path):
    print(f"❌ База не найдена: {db_path}")
else:
    conn = sqlite3.connect(db_path)
    table_name = 'app_gamemarketingdata'
    
    try:
        # 1. Узнаем, какие колонки реально есть в базе
        db_columns = get_table_columns(conn, table_name)
        print(f"✅ Найдено колонок в базе: {len(db_columns)}")

        # 2. Генерируем данные под эти колонки
        n_rows = 50
        data = {}
        
        for col in db_columns:
            if col == 'id': continue  # ID база заполнит сама
            if col == 'user_id':
                data[col] = [1] * n_rows
            elif col == 'date':
                data[col] = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(n_rows)]
            elif col in ['channel', 'country', 'os', 'platform']:
                data[col] = np.random.choice(['TikTok', 'Facebook', 'Google', 'iOS', 'Android', 'US', 'DE'], n_rows)
            elif 'factor' in col or 'retention' in col or col in ['spend', 'cost', 'revenue', 'iap_revenue', 'ad_revenue']:
                data[col] = np.random.uniform(0, 1000, n_rows).round(2)
            elif col in ['impressions', 'clicks', 'installs']:
                data[col] = np.random.randint(10, 10000, n_rows)
            else:
                # Для любых других колонок, которые мы не учли
                data[col] = 0

        df = pd.DataFrame(data)

        # 3. Загружаем
        print("📤 Загрузка данных...")
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print("💎 Данные загружены.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()