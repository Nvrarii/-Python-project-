from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Hall, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required  # только для админов (staff)
def all_bookings_view(request):
    bookings = Booking.objects.all().order_by('booking_date', 'start_time')
    return render(request, 'bookings/all_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    return redirect('bookings:my_bookings')

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('hall__gym')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

# View to handle booking
@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # теперь это твой кастомный User
            booking.save()
            messages.success(request, "Booking successful!")
            return redirect('bookings:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking.html', {'form': form})

# Confirmation view after a successful booking
@login_required
def booking_confirmation_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


# API to get booked slots between start and end dates
def api_booked_slots(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    try:
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)
    except Exception:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    if not start_dt or not end_dt:
        return JsonResponse({'error': 'Missing start or end parameter'}, status=400)

    bookings = Booking.objects.filter(
        booking_date__range=(start_dt.date(), end_dt.date()),
        status='active'  # если у модели Booking есть поле status
    )

    events = []
    for b in bookings:
        events.append({
            "start": f"{b.booking_date}T{b.start_time}",
            "end": f"{b.booking_date}T{b.end_time}",
            "title": f"Booking by {b.user.username}",
        })
    return JsonResponse(events, safe=False)

