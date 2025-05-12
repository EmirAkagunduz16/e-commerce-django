from django import forms

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=10)
    email = forms.EmailField()
    address_line_1 = forms.CharField(max_length=50)
    address_line_2 = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    order_note = forms.CharField(max_length=100, required=False)
    
    class Meta:
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'city', 'order_note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'  
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter Address Line 2'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Enter Order Note'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

