from django.shortcuts import render
from store.models import Product
from carts.models import CartItem
from .models import Order, OrderProduct, Payment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
import datetime
from decimal import Decimal


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Create Payment (uncomment and update)
            payment = Payment.objects.create(
                user=current_user,
                payment_id=order_number,  # Use a real payment ID if integrating PayPal/Stripe
                payment_method='Cash On Delivery',  # Update based on user choice
                amount_paid=grand_total,
                status='Completed'
            )
            data.payment = payment
            data.is_ordered = True  # Mark order as completed
            data.save()
            
            # Create OrderProduct entries (uncomment and update)
            for cart_item in cart_items:
                orderproduct = OrderProduct.objects.create(
                    order=data,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    user=current_user,
                    product_price=cart_item.product.price,
                    ordered=True,
                    payment=payment
                )
                # Reduce product stock
                product = Product.objects.get(id=cart_item.product.id)
                product.stock -= cart_item.quantity
                product.save()

            # Clear cart
            cart_items.delete()

            # Redirect to payments.html
            return redirect('payments')
        else:
            print(form.errors)

            # If form is not valid, show the form with errors
            return render(request, 'orders/place_order.html', {
                'form': form,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            })
    else:
        return redirect('checkout')

def payments(request):

    return render(request, 'orders/payments.html')

def order_complete(request):
    return render(request, 'orders/order_complete.html')

def order_details(request, order_id):
    return render(request, 'orders/order_details.html')

 # payment = Payment()
            # payment.user = current_user
            # payment.payment_id = 'temp'
            # payment.payment_method = 'Cash On Delivery'
            # payment.amount_paid = grand_total
            # payment.status = 'Accepted'
            # payment.save()
            # data.payment = payment
            # data.save()
            
            # for cart_item in cart_items:
            #     orderproduct = OrderProduct()
            #     orderproduct.order = data
            #     orderproduct.product = cart_item.product
            #     orderproduct.quantity = cart_item.quantity
            #     orderproduct.user = current_user
            #     orderproduct.product_price = cart_item.product.price
            #     orderproduct.ordered = True
            #     orderproduct.payment = payment
            #     orderproduct.save()
            #     product = Product.objects.get(id=cart_item.product_id)
            #     product.stock -= cart_item.quantity
            #     product.save()
            # cart_items.delete()
            # return redirect('payments')