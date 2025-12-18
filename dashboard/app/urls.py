from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_page, name='report'),
    path('', views.home_page, name='homepage'),
    path('login/', views.login_page, name='login'),
]
