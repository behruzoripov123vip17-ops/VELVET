from django.db import models


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('HOT', 'Hot Coffee'),
        ('COLD', 'Cold Coffee'),
        ('BAKERY', 'Bakery'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(MenuItem)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    TYPE_CHOICES = [
        ('REGULAR', 'Regular'),
        ('VIP', 'VIP Room'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    reservation_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='REGULAR')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.reservation_type} - {self.date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"



    

