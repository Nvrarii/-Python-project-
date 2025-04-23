from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),           # Главная страница
    path('about/', views.about, name='about'),    # Страница "О нас"
    path('contact/', views.contact, name='contact'),  # Страница "Контакты"

]
