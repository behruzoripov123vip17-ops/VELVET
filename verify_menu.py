import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from coffee.views import menu

def test_menu_view():
    factory = RequestFactory()
    request = factory.get('/menu/')
    request.session = {} 
    try:
        response = menu(request)
        if response.status_code == 200:
            print("[OK] Menu view rendered successfully with new template")
        else:
            print(f"[FAIL] Menu view returned {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Menu view failed: {e}")

if __name__ == '__main__':
    test_menu_view()
