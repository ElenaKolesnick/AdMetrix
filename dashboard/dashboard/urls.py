from django.contrib import admin
from django.urls import path, include
# Эти два импорта нужны здесь:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключение вашего файла, который мы правили выше:
    path('', include('app.urls')), 
]

# Код для аватарок добавляется ВНЕ списка urlpatterns, в самый конец:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)