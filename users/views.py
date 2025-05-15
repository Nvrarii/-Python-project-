from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from bookings.models import Booking
from .models import Profile
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

# Страница регистрации
def register_view(request):
    return render(request, 'registration/register.html')


# Обработка регистрации пользователя
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('users:profile')
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте введенные данные.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Страница входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('core:home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Редактирование профиля
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Убедись, что такой url существует
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})  # <-- путь исправлен

