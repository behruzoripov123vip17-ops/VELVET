import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from coffee.views import home, menu

def test_views():
    factory = RequestFactory()
    
    print("Testing Updated Views...")
    
    # Test Home
    try:
        request = factory.get('/')
        request.session = {} 
        response = home(request)
        if response.status_code == 200:
            print("[OK] Home view rendered successfully with new template")
        else:
            print(f"[FAIL] Home view returned {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Home view failed: {e}")

    # Test Menu (re-verify)
    try:
        request = factory.get('/menu/')
        request.session = {}
        response = menu(request)
        if response.status_code == 200:
            print("[OK] Menu view rendered successfully")
        else:
            print(f"[FAIL] Menu view returned {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Menu view failed: {e}")

if __name__ == '__main__':
    test_views()
