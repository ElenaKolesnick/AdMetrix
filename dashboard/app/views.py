import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache 

from .models import GameMarketingData, UserProfile 
from .forms import ProfileUpdateForm 

def home_page(request):
    """Отображение главной страницы с передачей профиля"""
    context = {}
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        context['profile'] = profile
    
    return render(request, 'homepage.html', context)

@login_required
@never_cache 
def report_page(request):
    """Формирование данных для аналитического дашборда"""
    queryset = GameMarketingData.objects.filter(user=request.user)
    
    print(f"\n[REPORT ACCESS] User: {request.user.username} | Records: {queryset.count()}")

    data_list = list(queryset.values(
        'date', 'channel', 'country', 'os', 
        'impressions', 'clicks', 'installs', 
        'spend', 'iap_revenue', 'ad_revenue', 'retention_d1'
    ))
    
    data_json = json.dumps(data_list, default=str)
    
    return render(request, 'report.html', {'data_json': data_json})

@login_required
def profile_view(request):
    """Просмотр и редактирование личного кабинета с поддержкой email"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # 1. Сохраняем email в модель User (так как поле в форме теперь есть)
            new_email = form.cleaned_data.get('email')
            if new_email:
                request.user.email = new_email
                request.user.save()

            # 2. Сохраняем остальные данные в UserProfile
            form.save()
            
            messages.success(request, "Профиль успешно обновлен!")
            return redirect('profile')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'profile.html', {'form': form})

def login_page(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('report') 

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('report')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_page(request):
    """Регистрация нового пользователя и создание профиля"""
    if request.user.is_authenticated:
        return redirect('report')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Аккаунт успешно создан!")
            return redirect('report')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    """Завершение сеанса пользователя"""
    if request.method == 'POST':
        logout(request)
    return redirect('homepage')