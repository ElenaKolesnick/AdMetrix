from django.urls import path
from app import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('report/', views.report_page, name='report'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'), # <-- Новая строка
]