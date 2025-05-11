from django.shortcuts import render, redirect   
from .forms import RegistrationForm, LoginForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Account
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user_name = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=user_name, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
            send_email.send()
            return redirect('/account/login?command=verification&email='+email)
        else:
            messages.error(request, form.errors)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                # messages.success(request, 'You are now logged in')
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('accounts:login')

    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('accounts:login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:register')
    

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    return render(request, 'accounts/reset_password.html')


# @login_required(login_url='login')
# @user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/dashboard.html', context)


# def forgot_password(request):
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             user = Account.objects.get(email=email) 
#             if user:
#                 # send reset password email
#                 pass
#             else:
#                 messages.error(request, 'User does not exist')
#                 return redirect('forgot_password')  
#     else:
#         form = ForgotPasswordForm()

#     context = {
#         'form': form
#     }
#     return render(request, 'accounts/forgot_password.html', context)    