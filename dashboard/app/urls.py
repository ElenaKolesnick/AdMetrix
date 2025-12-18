from app import views
from django.urls import path

urlpatterns = [
    path("", views.home_page, name="homepage"),
    path("report/", views.report_page, name="report"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # ДОБАВЛЯЕМ ЭТУ СТРОКУ:
    path("profile/", views.profile_view, name="profile"),
]
