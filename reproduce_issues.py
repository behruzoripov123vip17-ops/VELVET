import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from coffee.views import home, about, service, menu, contact, reservation, testimonial, cart_view

def test_views():
    factory = RequestFactory()
    
    views_to_test = [
        (home, 'home'),
        (about, 'about'),
        (service, 'service'),
        (menu, 'menu'),
        (contact, 'contact'),
        (reservation, 'reservation'),
        (testimonial, 'testimonial'),
        (cart_view, 'cart'),
    ]

    print("Testing views...")
    for view_func, name in views_to_test:
        try:
            request = factory.get(f'/{name}/')
            request.session = {} # Mock session
            response = view_func(request)
            if response.status_code == 200:
                print(f"[OK] {name}")
            else:
                print(f"[FAIL] {name} returned {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

if __name__ == '__main__':
    test_views()
