from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def booking(request):
    return render(request, 'core/booking.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')