from django.urls import path
from . import views

app_name = 'coffee'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('service/', views.service, name='service'),
    path('reservation/', views.reservation, name='reservation'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('menu/', views.menu, name='menu'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
]