from django.contrib import admin
from .models import Gym, Booking

# Register your models here.

# Регистрируем модели, чтобы они отображались в административной панели
admin.site.register(Gym)
admin.site.register(Booking)
