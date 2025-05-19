from django.urls import path
from . import views
from .views import all_bookings_view

app_name = 'bookings'

urlpatterns = [
    path('booking/', views.booking_view, name='booking'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('api/booked-slots/', views.api_booked_slots, name='api_booked_slots'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('admin/bookings/', all_bookings_view, name='all_bookings'),

]