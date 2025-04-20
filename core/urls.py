from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),          # Главная страница
    #path('booking/', views.booking, name='booking'),  # Страница бронирования
    path('about/', views.about, name='about'),      # Страница "О нас"
    path('contact/', views.contact, name='contact'),  # Страница "Контакты"
    path('register/', views.register_view, name='register'), # Страница регистрации
    #path('login/', views.login_view, name='login'), # Предполагаемый URL для входа
]