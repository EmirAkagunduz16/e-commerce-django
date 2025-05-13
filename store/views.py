from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Variation, ReviewRating
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewForm
from .models import ProductGallery
from django.contrib import messages
from django.shortcuts import redirect
from orders.models import OrderProduct

def store(request, category_slug=None):
  categories = None
  products = None
  
  if category_slug != None:
    categories = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=categories, is_available=True).order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
  else:
    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
 
  product_count = products.count()
  sizes = Variation.objects.sizes()  # Get all active sizes
  
  context = {
    'products': page_products,
    'product_count': product_count,
    'categories': categories,
    'sizes': sizes,  # Add sizes to context
  }
  return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
  try:
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
  except Exception as e:
    raise e
  
  try:
    if request.user.is_authenticated:
      orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    else:
      orderproduct = None
  except OrderProduct.DoesNotExist:
    orderproduct = None

  # get the reviews 
  reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

  # get the product gallery
  product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

  context = {
    'single_product': single_product,
    'in_cart': in_cart,
    'reviews': reviews,
    'orderproduct': orderproduct,
    'product_gallery': product_gallery,
   
  }
  return render(request, 'store/product_detail.html', context)

def search(request):
  products = Product.objects.none()  # Initialize with empty queryset
  product_count = 0
  page_products = products  # Initialize with empty queryset
  
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
      product_count = products.count()
      paginator = Paginator(products, 2)
      page = request.GET.get('page')
      page_products = paginator.get_page(page)
  
  context = {
    'products': page_products,
    'product_count': product_count,
  }
  return render(request, 'store/store.html', context)

def submit_review(request, product_id):
  url = request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
      form = ReviewForm(request.POST, instance=reviews)
      if form.is_valid():
        form.save()
        messages.success(request, 'Thank you! Your review has been submitted.')
        return redirect(url)
    except ReviewRating.DoesNotExist:
      form = ReviewForm(request.POST)
      if form.is_valid():
        data = ReviewRating()
        data.subject = form.cleaned_data['subject']
        data.rating = form.cleaned_data['rating']
        data.review = form.cleaned_data['review']
        data.ip = request.META.get('REMOTE_ADDR')
        data.product_id = product_id
        data.user_id = request.user.id
        data.save()
        messages.success(request, 'Thank you! Your review has been submitted.')
        return redirect(url)
    except Exception as e:
      print(e)
      messages.error(request, 'Error submitting review.')
      return redirect(url)   