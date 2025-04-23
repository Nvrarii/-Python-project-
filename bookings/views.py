from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Hall, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime

# View to handle booking
@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем бронирование
            messages.success(request, "Your booking was successful!")
            return redirect('bookings:booking_success')  # Переадресация на успешную страницу
    else:
        form = BookingForm()

    return render(request, 'bookings/booking.html', {'form': form})


# Confirmation view after a successful booking
def booking_confirmation_view(request, booking_id):
    # Fetch the Booking object by ID or return a 404 error
    booking = get_object_or_404(Booking, id=booking_id)

    context = {
        'booking': booking,  # Pass the booking object to the template
    }
    return render(request, 'bookings/booking_confirmation.html', context)  # Render the confirmation page


# API to get booked slots between start and end times
def api_booked_slots(request):
    start = request.GET.get('start')  # Get the start date
    end = request.GET.get('end')  # Get the end date

    # Convert strings to datetime objects
    start = parse_datetime(start)
    end = parse_datetime(end)

    # Get all bookings within the specified time range
    bookings = Booking.objects.filter(
        booking_date__range=(start, end),
        status='active'  # Assuming that active bookings have 'active' status
    )

    events = []
    for b in bookings:
        events.append({
            "start": f"{b.booking_date}T{b.start_time}",
            "end": f"{b.booking_date}T{b.end_time}",
            "title": f"Booking by {b.user.name}",
        })
    return JsonResponse(events, safe=False)
