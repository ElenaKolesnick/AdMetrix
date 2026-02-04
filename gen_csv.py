import csv
import random
from datetime import datetime, timedelta

# Настройки
num_rows = 50
channels = ['TikTok', 'Google Ads', 'Facebook Ads']
countries = ['USA', 'DEU', 'FRA', 'GBR', 'CAN']
filename = 'test_data_for_ml.csv'

columns = [
    'date', 'channel', 'country', 'os', 'spend', 
    'impressions', 'clicks', 'installs', 
    'iap_revenue', 'ad_revenue', 'retention_d1', 
    'cpi', 'roas', 'ltv'
]

start_date = datetime(2026, 1, 1)

with open(filename, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(columns) # Заголовки
    
    for i in range(num_rows):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        channel = random.choice(channels)
        country = random.choice(countries)
        
        # Генерация данных
        spend = round(random.uniform(200, 1500), 2)
        installs = random.randint(50, 300)
        
        # Выручка (обязательно не нулевая для ML!)
        iap_revenue = round(spend * random.uniform(0.8, 1.5), 2)
        ad_revenue = round(spend * random.uniform(0.1, 0.3), 2)
        
        total_rev = iap_revenue + ad_revenue
        
        row = [
            date, channel, country, 'Android', spend,
            installs * 10, installs * 2, installs,
            iap_revenue, ad_revenue,
            round(random.uniform(25, 35), 2),     # retention
            round(spend / installs, 2),          # cpi
            round(total_rev / spend, 2),         # roas
            round(total_rev / installs, 2)       # ltv
        ]
        writer.writerow(row)

print(f"Готово! Файл '{filename}' создан без использования сторонних библиотек.")