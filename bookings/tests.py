import pytest
from django.contrib.auth import get_user_model
from bookings.models import Booking, Gym, Hall, Schedule
from datetime import date, time

User = get_user_model()

@pytest.mark.django_db
def test_create_booking():
    user = User.objects.create_user(email='bookinguser@example.com', name='Test User', password='12345')

    gym = Gym.objects.create(
        name='Test Gym',
        location='Test City',
        description='A test gym',
        contact_phone='1234567890'
    )

    hall = Hall.objects.create(
        gym=gym,
        name='Main Hall',
        description='Big main hall',
        capacity=50,
        type='Fitness',
        image_url=None
    )

    schedule = Schedule.objects.create(
        hall=hall,
        day_of_week=1,        # Вторник (0 — Monday, 1 — Tuesday ...)
        open_time=time(10, 0),
        close_time=time(11, 0)
    )

    booking = Booking.objects.create(
        user=user,
        hall=hall,
        booking_date=date.today(),
        start_time=time(10, 0),
        end_time=time(11, 0),
        status='pending'
    )

    assert booking in Booking.objects.all()
