import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm  # Импортируем форму профиля
from .models import GameMarketingData, UserProfile  # Импортируем обе модели


def home_page(request):
    """Главная страница"""
    return render(request, "homepage.html", {})


@login_required
def report_page(request):
    """Страница с аналитическими отчетами (Flexmonster)"""
    # Фильтруем данные: каждый пользователь видит только свои записи
    raw_data = list(GameMarketingData.objects.filter(user=request.user).values())
    data_json = json.dumps(raw_data, default=str)

    return render(request, "report.html", {"data_json": data_json})


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print("Данные успешно сохранены!")  # Отладка
            return redirect("profile")
        else:
            print("Ошибки формы:", form.errors)  # Это покажет причину в терминале
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "profile.html", {"form": form})


def login_page(request):
    """Авторизация"""
    if request.user.is_authenticated:
        return redirect("profile")  # После входа ведем в профиль

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def register_page(request):
    """Регистрация"""
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически создаем профиль при регистрации
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("profile")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    """Выход"""
    if request.method == "POST":
        logout(request)
    return redirect("homepage")
