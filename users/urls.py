from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/user/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
