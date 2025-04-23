from django import forms
from .models import Hall, Booking
from django.core.exceptions import ValidationError
from django.utils import timezone  # For date comparisons

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hall', 'booking_date', 'start_time', 'end_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': '3600'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'step': '3600'}),
        }
        labels = {
            'hall': 'Выберите зал',
            'booking_date': 'Дата бронирования',
            'start_time': 'Время начала',
            'end_time': 'Время окончания',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hall'].queryset = Hall.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        booking_date = cleaned_data.get('booking_date')
        hall = cleaned_data.get('hall')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Время начала должно быть раньше времени окончания.")
            if start_time == end_time:
                raise forms.ValidationError("Время начала и окончания не должны совпадать.")

        if booking_date and booking_date < timezone.now().date():
            raise forms.ValidationError("Дата бронирования не может быть в прошлом.")

        #  Check for overlapping bookings (This is a simplified check, you might need a more complex one)
        if hall and booking_date and start_time and end_time:
            overlapping_bookings = Booking.objects.filter(
                hall=hall,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(pk=self.instance.pk if self.instance else None)  # Exclude the current instance if it's an update
            if overlapping_bookings.exists():
                raise forms.ValidationError("Выбранное время уже занято.")

        return cleaned_data
