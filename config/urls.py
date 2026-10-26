from django.contrib import admin
from django.urls import path

from .views import health_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('health/', health_view, name='health'),
    path('admin/', admin.site.urls),
]
