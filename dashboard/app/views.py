from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def home_page(request):
    """Отображение главной страницы"""
    return render(request, 'homepage.html', {})

def report_page(request):
    """Личный кабинет с отчетами"""
    # Защита: если неавторизованный пользователь пытается зайти на /report/
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'report.html', {})

def login_page(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('report') # Перенаправляем авторизованных сразу в кабинет

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('report') # Изменено с 'homepage' на 'report'
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_view(request):
    """Выход из системы"""
    if request.method == 'POST':
        logout(request)
    return redirect('homepage') # После выхода логично вернуть на главную

def register_page(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('report') # Перенаправляем авторизованных сразу в кабинет

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('report') # Изменено с 'homepage' на 'report'
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)