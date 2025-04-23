from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Hall, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime


# @login_required  # Uncomment if you want to require login to book
def booking_view(request):
    halls = Hall.objects.all()  # Get all halls from the database

    # If the user is sending the form data (POST request)
    if request.method == 'POST':
        form = BookingForm(request.POST)  # Create a form instance with the submitted data
        if form.is_valid():
            booking = form.save(commit=False)  # Create a Booking object but don't save it yet
            # booking.user = request.user  # Assign the logged-in user (if using authentication)
            booking.save()  # Save the Booking object to the database
            messages.success(request, "Бронирование успешно создано!")  # Display a success message
            return redirect('bookings:booking_confirmation', booking_id=booking.id)  # Redirect to confirmation page
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")  # Display an error message
    else:
        form = BookingForm()  # Create an empty form instance

    # Pass the halls and form to the template
    context = {
        'halls': halls,
        'form': form,
    }
    return render(request, 'bookings/booking.html', context)  # Render the booking form


def booking_confirmation_view(request, booking_id):
    # Fetch the Booking object by ID or return a 404 error
    booking = get_object_or_404(Booking, id=booking_id)

    context = {
        'booking': booking,  # Pass the booking object to the template
    }
    return render(request, 'bookings/booking_confirmation.html', context)  # Render the confirmation page


# API to get booked slots between start and end times
def api_booked_slots(request):
    start = request.GET.get('start')  # Получаем начальную дату
    end = request.GET.get('end')  # Получаем конечную дату

    # Преобразуем строки в объекты datetime
    start = parse_datetime(start)
    end = parse_datetime(end)

    # Получаем все бронирования в заданном интервале времени
    bookings = Booking.objects.filter(
        booking_date__range=(start, end),
        status='active'  # Здесь предполагается, что активные бронирования имеют статус 'active'
    )

    events = []
    for b in bookings:
        events.append({
            "start": f"{b.booking_date}T{b.start_time}",
            "end": f"{b.booking_date}T{b.end_time}",
            "title": f"Booking by {b.user.name}",
        })
    return JsonResponse(events, safe=False)
