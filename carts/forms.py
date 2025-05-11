from django import forms
from .models import Order
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist   

PAYMENT_METHODS = [
    ('cod', 'Cash On Delivery'),
    ('razorpay', 'Razorpay'),
]
    
class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10)
    email = forms.EmailField()
    address_line_1 = forms.CharField(max_length=50)
    address_line_2 = forms.CharField(max_length=50) 
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    order_note = forms.CharField(max_length=100, required=False)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'order_note', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter Address Line 2'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter State'
        self.fields['payment_method'].widget.attrs['placeholder'] = 'Select Payment Method'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(CheckoutForm, self).clean()
        if not self.errors:
            try:
                user = User.objects.get(email=cleaned_data['email'])
                if user:
                    raise forms.ValidationError("Email already exists") 
            except ObjectDoesNotExist:
                pass
        return cleaned_data
    
