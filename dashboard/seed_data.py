import os
import random
from datetime import datetime, timedelta

import django

# Установка окружения Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
django.setup()

from app.models import GameMarketingData
from django.contrib.auth.models import User


def seed_db():
    # Получаем всех существующих пользователей
    all_users = User.objects.all()

    if not all_users.exists():
        print("Ошибка: В базе нет пользователей. Сначала зарегистрируйтесь на сайте!")
        return

    channels = ["Facebook Ads", "Google Ads", "TikTok", "Unity Ads", "IronSource"]
    countries = ["USA", "Germany", "UK", "Brazil", "Japan", "Korea", "Canada"]
    platforms = ["iOS", "Android"]

    print(f"Начинаю загрузку данных для {all_users.count()} пользователей...")

    for user in all_users:
        # Создаем по 15 записей для каждого пользователя
        for _ in range(15):
            country = random.choice(countries)
            multiplier = 2.5 if country in ["USA", "Japan"] else 1.0

            installs = random.randint(50, 600)
            clicks = int(installs * random.uniform(1.2, 2.8))

            GameMarketingData.objects.create(
                user=user,  # Привязываем к конкретному юзеру
                date=datetime.now().date() - timedelta(days=random.randint(0, 30)),
                channel=random.choice(channels),
                country=country,
                os=random.choice(platforms),
                impressions=clicks * random.randint(5, 10),
                clicks=clicks,
                installs=installs,
                spend=round(installs * random.uniform(0.7, 2.0) * multiplier, 2),
                iap_revenue=round(installs * random.uniform(0.3, 3.0) * multiplier, 2),
                ad_revenue=round(installs * random.uniform(0.05, 0.2), 2),
                retention_d1=round(random.uniform(20.0, 50.0), 1),
            )
        print(f"--- Данные для пользователя {user.username} добавлены.")

    print("\nГотово! База полностью обновлена.")


if __name__ == "__main__":
    seed_db()
