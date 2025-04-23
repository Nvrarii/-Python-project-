from django.contrib import admin
from .models import Gym, Booking, Hall

# Register your models here.

# Регистрируем модели, чтобы они отображались в административной панели
admin.site.register(Gym)
admin.site.register(Booking)

@admin.register(Hall)  # Регистрация модели Hall в админке
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'capacity', 'type', 'description')  # Настроить отображаемые поля
    search_fields = ('name', 'gym__name')  # Настроить поиск по этим полям
    list_filter = ('gym', 'type')  # Добавить фильтры для админки
