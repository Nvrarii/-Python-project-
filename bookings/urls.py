from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('booking/', views.booking_view, name='booking'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('api/booked-slots/', views.api_booked_slots, name='api_booked_slots')
]