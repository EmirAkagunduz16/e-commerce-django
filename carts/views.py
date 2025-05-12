from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required       

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        color_val = request.POST.get('color')
        size_val  = request.POST.get('size')

        product_variation = []
        if color_val:
            try:
                var = Variation.objects.get(
                    product=product,
                    variation_category__iexact='color',
                    variation_value__iexact=color_val
                )
                product_variation.append(var)
            except Variation.DoesNotExist:
                pass

        if size_val:
            try:
                var = Variation.objects.get(
                    product=product,
                    variation_category__iexact='size',
                    variation_value__iexact=size_val
                )
                product_variation.append(var)
            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        id_list = []
        for item in cart_item:
            existing_variations = item.variations.all()
            # Collect variation IDs and sort them for consistent comparison
            ex_var_ids = sorted([var.id for var in existing_variations])
            ex_var_list.append(ex_var_ids)
            id_list.append(item.id)

        # Sort current product variations' IDs
        current_var_ids = sorted([var.id for var in product_variation])

        if current_var_ids in ex_var_list:
            # Existing item found: increment quantity
            index = ex_var_list.index(current_var_ids)
            item_id = id_list[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # Create new cart item with variations
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception as e:
        pass
    
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        total_price = float(total) + float(tax)    
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'total_price': total_price,
        }
        return render(request, 'store/cart.html', context)
    except ObjectDoesNotExist:
        # Return an empty cart page when no cart exists
        context = {
            'total': 0,
            'quantity': 0,
            'cart_items': [],
            'tax': 0,
            'total_price': 0,
        }
        return render(request, 'store/cart.html', context)

@login_required(login_url='accounts:login')
def checkout(request):
    form = CheckoutForm()
    try:
        total = 0
        quantity = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        total = total + tax
        total_price = float(total) + float(tax)
    except ObjectDoesNotExist:
        return redirect('store')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def place_order(request):

    return render(request, 'store/place_order.html')    