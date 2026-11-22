from django import forms
from .models import Order

CITY_CHOICES = [
    ('Kathmandu', 'Kathmandu Valley (NPR 100 Delivery - 24 to 48 hrs)'),
    ('Lalitpur', 'Lalitpur (NPR 100 Delivery - 24 to 48 hrs)'),
    ('Bhaktapur', 'Bhaktapur (NPR 100 Delivery - 24 to 48 hrs)'),
    ('Pokhara', 'Pokhara (NPR 180 Courier Delivery - 2 to 3 days)'),
    ('Chitwan', 'Chitwan (NPR 180 Courier Delivery - 2 to 3 days)'),
    ('Butwal', 'Butwal (NPR 180 Courier Delivery - 2 to 3 days)'),
    ('Biratnagar', 'Biratnagar (NPR 180 Courier Delivery - 3 to 4 days)'),
    ('Dharan', 'Dharan (NPR 180 Courier Delivery - 3 to 4 days)'),
    ('Other Nepal Location', 'Other Nepal District (NPR 180 Courier Delivery)'),
]

class CheckoutForm(forms.ModelForm):
    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'citySelect'})
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'city', 'delivery_address', 'order_notes', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98XXXXXXXX'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, Tole, House/Apartment No.'}),
            'order_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Delivery instructions, e.g. landmark near gate'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'btn-check'}),
        }
