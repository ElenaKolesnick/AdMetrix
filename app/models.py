from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- МОДЕЛЬ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ ---

class UserProfile(models.Model):
    PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Indie', 'Indie'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    full_name = models.CharField(max_length=255, blank=True, verbose_name="Имя и Фамилия")
    company_name = models.CharField(max_length=255, blank=True, verbose_name="Компания")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    about = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    website = models.URLField(blank=True, verbose_name="Сайт проекта")
    industry = models.CharField(max_length=100, blank=True, verbose_name="Индустрия")
    timezone = models.CharField(max_length=100, default="Moscow Time (UTC+3)", verbose_name="Часовой пояс")
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='Free', verbose_name="Тариф")
    subscription_end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания подписки")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль: {self.user.username} ({self.subscription_plan})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# --- МОДЕЛЬ МАРКЕТИНГОВЫХ ДАННЫХ ---

class GameMarketingData(models.Model):
    """Модель маркетинговых данных для AdMetrix"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    date = models.DateField("Дата")
    channel = models.CharField("Канал", max_length=50)
    country = models.CharField("Страна (ISO)", max_length=3)
    os = models.CharField("ОС", max_length=20, default="Android")
    
    # Основные финансовые показатели
    iap_revenue = models.FloatField("Доход IAP ($)", default=0.0, null=True, blank=True)
    ad_revenue = models.FloatField("Доход с рекламы ($)", default=0.0, null=True, blank=True)
    spend = models.FloatField("Затраты ($)", default=0.0, null=True, blank=True)
    installs = models.IntegerField("Установки", default=0)
    
    # Технические метрики
    impressions = models.IntegerField("Показы", default=0)
    clicks = models.IntegerField("Клики", default=0)
    
    # Ключевые аналитические показатели (вынесены для быстрой выборки)
    cpi = models.FloatField("CPI", default=0.0)
    roas = models.FloatField("ROAS", default=0.0)
    ltv = models.FloatField("LTV", default=0.0)
    retention_d1 = models.FloatField("Retention D1", default=0.0)

    # Резервный блок: факторы для машинного обучения (m01 - m40)
    # Мы прописываем их все, чтобы импорт 40+ метрик работал без ошибок
    m01 = models.FloatField(default=0.0)
    m02 = models.FloatField(default=0.0)
    m03 = models.FloatField(default=0.0)
    m04 = models.FloatField(default=0.0)
    m05 = models.FloatField(default=0.0)
    m06 = models.FloatField(default=0.0)
    m07 = models.FloatField(default=0.0)
    m08 = models.FloatField(default=0.0)
    m09 = models.FloatField(default=0.0)
    m10 = models.FloatField(default=0.0)
    m11 = models.FloatField(default=0.0)
    m12 = models.FloatField(default=0.0)
    m13 = models.FloatField(default=0.0)
    m14 = models.FloatField(default=0.0)
    m15 = models.FloatField(default=0.0)
    m16 = models.FloatField(default=0.0)
    m17 = models.FloatField(default=0.0)
    m18 = models.FloatField(default=0.0)
    m19 = models.FloatField(default=0.0)
    m20 = models.FloatField(default=0.0)
    m21 = models.FloatField(default=0.0)
    m22 = models.FloatField(default=0.0)
    m23 = models.FloatField(default=0.0)
    m24 = models.FloatField(default=0.0)
    m25 = models.FloatField(default=0.0)
    m26 = models.FloatField(default=0.0)
    m27 = models.FloatField(default=0.0)
    m28 = models.FloatField(default=0.0)
    m29 = models.FloatField(default=0.0)
    m30 = models.FloatField(default=0.0)
    m31 = models.FloatField(default=0.0)
    m32 = models.FloatField(default=0.0)
    m33 = models.FloatField(default=0.0)
    m34 = models.FloatField(default=0.0)
    m35 = models.FloatField(default=0.0)
    m36 = models.FloatField(default=0.0)
    m37 = models.FloatField(default=0.0)
    m38 = models.FloatField(default=0.0)
    m39 = models.FloatField(default=0.0)
    m40 = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = "Маркетинговые данные"
        verbose_name_plural = "Маркетинговые данные"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} | {self.channel} | {self.country}"

    @property
    def total_revenue(self):
        # Защита от сложения числа с None
        iap = self.iap_revenue or 0.0
        ad = self.ad_revenue or 0.0
        return iap + ad