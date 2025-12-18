from django.contrib import admin
from .models import UserProfile, GameMarketingData

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_plan', 'subscription_end_date']
    list_editable = ['subscription_plan', 'subscription_end_date'] # Можно менять прямо в списке