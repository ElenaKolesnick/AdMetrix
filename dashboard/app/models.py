from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Модель расширенного профиля пользователя (Личный кабинет)"""
    PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Indie', 'Indie'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    
    # Личные данные
    full_name = models.CharField(max_length=255, blank=True, verbose_name="Имя и Фамилия")
    company_name = models.CharField(max_length=255, blank=True, verbose_name="Компания")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    about = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    
    # Настройки проекта и подписки
    website = models.URLField(blank=True, verbose_name="Сайт проекта")
    industry = models.CharField(max_length=100, blank=True, verbose_name="Индустрия")
    timezone = models.CharField(max_length=100, default="Moscow Time (UTC+3)", verbose_name="Часовой пояс")
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='Free', verbose_name="Тариф")
    subscription_end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания подписки")

    def __str__(self):
        return f"Профиль: {self.user.username} ({self.subscription_plan})"


class GameMarketingData(models.Model):
    """Модель маркетинговых данных для дашборда"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    date = models.DateField("Дата")
    channel = models.CharField("Канал", max_length=50)
    country = models.CharField("Страна", max_length=50)
    os = models.CharField("ОС", max_length=20)
    
    # Метрики
    impressions = models.IntegerField("Показы")
    clicks = models.IntegerField("Клики")
    installs = models.IntegerField("Установки")
    spend = models.FloatField("Затраты ($)")
    iap_revenue = models.FloatField("Доход IAP ($)")
    ad_revenue = models.FloatField("Доход с рекламы ($)")
    retention_d1 = models.FloatField("Retention Day 1 (%)")

    def __str__(self):
        return f"{self.user.username} | {self.channel} | {self.date}"