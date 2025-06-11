from django import forms

from event_system.models import Booking, Hall, Payment

class BookingForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )
    end_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )

    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'start_datetime', 'end_datetime']



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        card_number = cleaned_data.get('card_number')
        upi_id = cleaned_data.get('upi_id')

        if payment_method == 'debit_card' and not card_number:
            self.add_error('card_number', 'Card number is required for debit card payments.')
        elif payment_method == 'upi' and not upi_id:
            self.add_error('upi_id', 'UPI ID is required for UPI payments.')    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
             'placeholder': 'Enter your name on your card or UPI account'
        })  

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = "__all__"        