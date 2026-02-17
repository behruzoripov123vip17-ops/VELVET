from coffee.models import MenuItem

def seed():
    MenuItem.objects.all().delete()
    print("Deleted all existing menu items.")

    menu_items = [
        MenuItem(name='Matcha Latte', description='Premium ceremonial grade matcha', price=6.50, category='HOT'),
        MenuItem(name='Hojicha', description='Roasted green tea', price=5.00, category='HOT'),
        MenuItem(name='Sakura Cold Brew', description='Cold brew with cherry blossom essence', price=7.00, category='COLD'),
        MenuItem(name='Iced Coffee', description='Traditional japanese iced coffee', price=5.50, category='COLD'),
    ]

    for item in menu_items:
        item.save()

    print("Database seeded with sample MenuItems!")

if __name__ == '__main__':
    seed()
