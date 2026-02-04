import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_smart_data():
    date_range = pd.date_range(start="2025-01-01", end="2025-12-31")
    channels = ['TikTok', 'Google Ads', 'Facebook Ads']
    countries = ['USA', 'DEU', 'FRA', 'GBR', 'CAN']
    platforms = ['iOS', 'Android']
    
    data = []
    
    for date in date_range:
        # Сезонный коэффициент (зимой и в конце месяца тратим больше)
        month_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)
        
        for channel in channels:
            for country in countries:
                for os in platforms:
                    # Базовые затраты с шумом
                    base_spend = np.random.uniform(100, 500) * month_factor
                    
                    # Логика CPI: чем больше тратим, тем дороже инсталл
                    # (ML модель должна это заметить)
                    cpi = np.random.uniform(0.5, 1.5) + (base_spend / 1000)
                    installs = int(base_spend / cpi)
                    
                    # Логика выручки: LTV зависит от канала и страны
                    if country == 'USA': ltv = np.random.uniform(2.5, 4.0)
                    else: ltv = np.random.uniform(1.5, 3.0)
                    
                    # В TikTok выручка более хаотична (для сложности обучения)
                    if channel == 'TikTok': ltv *= np.random.uniform(0.7, 1.5)
                    
                    revenue = installs * ltv
                    
                    row = {
                        'date': date.strftime('%Y-%m-%d'),
                        'channel': channel,
                        'country': country,
                        'platform': os,
                        'spend': round(base_spend, 2),
                        'impressions': installs * np.random.randint(50, 100),
                        'clicks': installs * np.random.randint(2, 5),
                        'installs': installs,
                        'iap_revenue': round(revenue, 2),
                        'user_id': 1
                    }
                    
                    # Добавляем пустые метрики, как в твоем исходнике
                    for i in range(1, 41):
                        row[f'metric_factor_{i:02d}'] = round(np.random.uniform(0, 100), 4)
                        
                    data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv('marketing_2025_super.csv', index=False)
    print(f"Файл создан! Строк: {len(df)}")

if __name__ == "__main__":
    generate_smart_data()