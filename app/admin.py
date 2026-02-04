from django.contrib import admin
from .models import UserProfile, GameMarketingData

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_plan', 'subscription_end_date']
    list_editable = ['subscription_plan', 'subscription_end_date']
    search_fields = ['user__username', 'company_name']

@admin.register(GameMarketingData)
class GameMarketingDataAdmin(admin.ModelAdmin):
    # Автоматически получаем список всех полей модели
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields if field.name != 'id']

    # Добавляем фильтры по ключевым полям
    list_filter = ['channel', 'os', 'country', 'date']
    
    # Поиск по каналу или имени пользователя
    search_fields = ['channel', 'user__username']
    
    # Разбивка на страницы (по 20 записей), чтобы 56 колонок не тормозили браузер
    list_per_page = 20

    # Опционально: делаем таблицу компактнее в админке
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }