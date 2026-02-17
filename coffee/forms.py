from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'guests', 'reservation_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control p-4', 'placeholder': 'Email'}),
            'date': forms.DateInput(attrs={'class': 'form-control p-4 datetimepicker-input', 'placeholder': 'Date', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control p-4 datetimepicker-input', 'placeholder': 'Time', 'type': 'time'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control p-4', 'placeholder': 'Guests', 'min': 1}),
            'reservation_type': forms.Select(attrs={'class': 'form-control px-4', 'style': 'height: 49px;'}),
        }
