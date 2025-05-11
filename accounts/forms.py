from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!") 

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password
        
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = Account.objects.filter(email=email).first()
            if user is None or not user.check_password(password):
                raise forms.ValidationError("Invalid login credentials")
            else:
                return cleaned_data 
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password

        

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Email',
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password != self.cleaned_data.get('password'):
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
     

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password != self.cleaned_data.get('password'):
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

