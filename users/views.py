
from django.shortcuts import render, redirect

def register_view(request):
    return render(request, 'registration/register.html')
def register_user(request):
    if request.method == 'POST':
        # Здесь будет логика обработки данных формы регистрации
        print("Данные формы регистрации получены!")
        return redirect('home')  # Или на другую страницу после регистрации
    else:
        return redirect('register') # Если кто-то попытается получить доступ к URL методом GET
      
def login_view(request):
    # Здесь будет логика отображения формы входа
    return render(request, 'users/login.html') # Вам нужно будет создать этот шаблон
