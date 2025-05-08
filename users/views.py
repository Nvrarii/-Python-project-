from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from bookings.models import Booking  # Правильный путь к модели Booking
from .models import Profile
from .forms import ProfileForm  # Создай, если ещё нет

# Страница регистрации
def register_view(request):
    return render(request, 'registration/register.html')

# Обработка регистрации пользователя
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('users:profile')  # Переход на профиль
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
            # Авторизуем пользователя
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('core:home')  # редирект на главную страницу после успешного входа
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})

# Страница бронирования
def booking_view(request):
    if request.method == 'POST':
        booking = Booking(
            user=request.user,
            hall_id=request.POST.get('hall'),
            booking_date=request.POST.get('booking_date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
        booking.save()
        messages.success(request, "Your booking was successful!")
        return redirect('bookings:success')  # Переадресация на страницу успешного бронирования
    return render(request, 'bookings/booking.html')  # Используем существующий шаблон booking.html

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')
