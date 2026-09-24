from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, Reservation, ContactMessage
from .forms import ReservationForm


def home(request):
    items = MenuItem.objects.all()
    form = ReservationForm()
    return render(request, "index.html", {
        "hot_coffee": items.filter(category="HOT"),
        "cold_coffee": items.filter(category="COLD"),
        "bakery": items.filter(category="BAKERY"),
        "form": form,
    })


def contact_submit(request):
    if request.method == "POST":
        data = {key: request.POST.get(key) for key in ("name", "email", "subject", "message")}
        if all(data.values()):
            ContactMessage.objects.create(**data)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Missing data"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def about(request):
    return render(request, "about.html")


def menu(request):
    items = MenuItem.objects.all().order_by("name")
    category, search = request.GET.get("category"), request.GET.get("search")
    if search:
        items = items.filter(name__icontains=search)
    if category:
        items = items.filter(category=category)
    paginator = Paginator(items, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    hot_coffee = [i for i in page_obj if i.category == "HOT"] if not category or category == "HOT" else []
    cold_coffee = [i for i in page_obj if i.category == "COLD"] if not category or category == "COLD" else []
    bakery = [i for i in page_obj if i.category == "BAKERY"] if not category or category == "BAKERY" else []
    return render(request, "menu.html", {
        "hot_coffee": hot_coffee, "cold_coffee": cold_coffee, "bakery": bakery,
        "page_obj": page_obj, "category": category,
    })


def add_to_cart(request, item_id):
    request.session.setdefault("cart", []).append(item_id)
    request.session.modified = True
    get_object_or_404(MenuItem, id=item_id)
    messages.success(request, "Item added to cart!")
    return redirect("coffee:menu")


def cart_view(request):
    cart_ids = request.session.get("cart", [])
    display_items, total_price, valid_cart_ids = [], 0, []
    for item_id in cart_ids:
        try:
            item = MenuItem.objects.get(id=item_id)
            display_items.append(item)
            total_price += item.price
            valid_cart_ids.append(item_id)
        except MenuItem.DoesNotExist:
            pass
    if len(valid_cart_ids) != len(cart_ids):
        request.session["cart"] = valid_cart_ids
        request.session.modified = True
    if request.method == "POST":
        if not display_items:
            messages.error(request, "Cart is empty")
            return redirect("coffee:menu")
        order = Order.objects.create(total_price=total_price, status="Pending")
        order.items.set(display_items)
        request.session["cart"] = []
        messages.success(request, "Order placed successfully!")
        return redirect("coffee:menu")
    return render(request, "cart.html", {"cart_items": display_items, "total_price": total_price})


def contact(request):
    return render(request, "contact.html")


def service(request):
    return render(request, "service.html")


def reservation(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            request.session["login_next"] = "/reservation/"
            return redirect("users:google_login")
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation_obj = form.save(commit=False)
            reservation_obj.user = request.user
            reservation_obj.email = request.user.email
            reservation_obj.name = request.user.get_full_name() or request.user.username
            reservation_obj.save()
            messages.success(request, "Your reservation has been booked successfully!")
            return redirect("coffee:reservation")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        form = ReservationForm(initial=initial)
    return render(request, "reservation.html", {"form": form})


def testimonial(request):
    return render(request, "testimonial.html")
