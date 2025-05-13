from django.shortcuts import render, redirect   
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm
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
from .forms import ResetPasswordForm
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order
import requests
from django.db.models import Count
from accounts.models import UserProfile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            profile_picture = form.cleaned_data.get('profile_picture')
            password = form.cleaned_data.get('password')
            user_name = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=user_name, email=email, password=password)
            user.phone_number = phone_number
            user.profile_picture = profile_picture
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

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                session_cart_items = CartItem.objects.filter(cart=cart)
                
                # Merge session cart items into user's cart
                for session_item in session_cart_items:
                    # Get session item variations sorted by category
                    session_variations = list(session_item.variations.all().order_by('variation_category'))
                    
                    # Check for existing items in user's cart with same product and variations
                    user_cart_items = CartItem.objects.filter(user=user, product=session_item.product)
                    match_found = False
                    
                    for user_item in user_cart_items:
                        # Get user item variations sorted by category
                        user_item_variations = list(user_item.variations.all().order_by('variation_category'))
                        
                        if user_item_variations == session_variations:
                            # Merge quantities
                            user_item.quantity += session_item.quantity
                            user_item.save()
                            session_item.delete()  # Remove the session item
                            match_found = True
                            break
                    
                    if not match_found:
                        # Assign the session item to the user
                        session_item.user = user
                        session_item.cart = None
                        session_item.save()
                        
                # Delete the session cart after merging
                cart.delete()
            except Cart.DoesNotExist:
                pass
            
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    return redirect(params['next'])
            except:
                return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('accounts:login')
    
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url = 'accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
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
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Reset Password Email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('accounts:forgot_password')
    else:
        form = ForgotPasswordForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/forgot_password.html', context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has expired')
        return redirect('accounts:forgot_password')
    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if password == confirm_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Passwords do not match')   
    else:
        form = ResetPasswordForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/reset_password.html', context)
         
        
@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)