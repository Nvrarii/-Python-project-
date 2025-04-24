from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),  # Добавьте этот путь
    
]
