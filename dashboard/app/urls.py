from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('report/', views.report_page, name='report'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
]