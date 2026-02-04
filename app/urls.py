from django.urls import path
from . import views

urlpatterns = [
    # 1. Публичный лендинг (виден всем при входе на сайт)
    path('', views.home_page, name='homepage'), 
    
    # 2. Рабочая панель (Dashboard / Index) - доступна после входа
    path('dashboard/', views.index_page, name='dashboard_index'), 

    # 3. Остальные разделы приложения
    path('report/', views.report_page, name='report'), 
    path('import/', views.import_page, name='import'),
    path('learning/', views.learning_page, name='learning'),
    path('profile/', views.profile_view, name='profile'),
    
    # 4. Система аутентификации
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
]