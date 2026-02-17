from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import MenuItem, Order, Reservation, ContactMessage
from .forms import ReservationForm

# Create your views here.
def home(request):
    items = MenuItem.objects.all()
    hot_coffee = items.filter(category='HOT')
    cold_coffee = items.filter(category='COLD')
    bakery = items.filter(category='BAKERY')
    form = ReservationForm()
    
    context = {
        'hot_coffee': hot_coffee,
        'cold_coffee': cold_coffee,
        'bakery': bakery,
        'form': form,
    }
    return render(request, 'index.html', context)

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def about(request):
    return render(request, 'about.html')

def menu(request):
    # Base queryset - get all items ordered by name
    items = MenuItem.objects.all().order_by('name')
    
    # Get the category filter (if any)
    category = request.GET.get('category')
    
    # Filter by search query if provided
    search = request.GET.get('search')
    if search:
        items = items.filter(name__icontains=search)
    
    # Filter by category if provided - do this BEFORE pagination
    if category:
        items = items.filter(category=category)
    
    # Pagination - after all filtering
    paginator = Paginator(items, 8) # Show 8 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # If category is selected, populate the corresponding list
    # If no category is selected, organize items by category for display
    if category == 'HOT':
        hot_coffee = list(page_obj)
        cold_coffee = []
        bakery = []
    elif category == 'COLD':
        hot_coffee = []
        cold_coffee = list(page_obj)
        bakery = []
    elif category == 'BAKERY':
        hot_coffee = []
        cold_coffee = []
        bakery = list(page_obj)
    else:
        # Filter current page items by category
        hot_coffee = [i for i in page_obj if i.category == 'HOT']
        cold_coffee = [i for i in page_obj if i.category == 'COLD']
        bakery = [i for i in page_obj if i.category == 'BAKERY']
    
    context = {
        'hot_coffee': hot_coffee,
        'cold_coffee': cold_coffee,
        'bakery': bakery,
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'menu.html', context)

def add_to_cart(request, item_id):
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    # Verify item exists before adding
    get_object_or_404(MenuItem, id=item_id)
    
    request.session['cart'].append(item_id)
    request.session.modified = True
    messages.success(request, 'Item added to cart!')
    return redirect('coffee:menu')

def cart_view(request):
    cart_ids = request.session.get('cart', [])
    display_items = []
    total_price = 0
    
    # Handle potentially missing items
    valid_cart_ids = []
    for item_id in cart_ids:
        try:
            item = MenuItem.objects.get(id=item_id)
            display_items.append(item)
            total_price += item.price
            valid_cart_ids.append(item_id)
        except MenuItem.DoesNotExist:
            continue
    
    # Update session if any items were missing
    if len(valid_cart_ids) != len(cart_ids):
        request.session['cart'] = valid_cart_ids
        request.session.modified = True

    if request.method == 'POST':
        if not display_items:
            messages.error(request, 'Cart is empty')
            return redirect('coffee:menu')
            
        order = Order.objects.create(total_price=total_price, status='Pending')
        order.items.set(display_items)
        order.save()
        
        request.session['cart'] = []
        messages.success(request, 'Order placed successfully!')
        return redirect('coffee:menu')

    return render(request, 'cart.html', {'cart_items': display_items, 'total_price': total_price})

def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'service.html')

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your reservation has been booked successfully!')
            return redirect('coffee:reservation')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})

def testimonial(request):
    return render(request, 'testimonial.html')


