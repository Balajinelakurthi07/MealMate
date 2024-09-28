# models.py
from django.db import models
from django.contrib.auth.models import User
from .utils import user_directory_path

class MenuSection(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    section = models.ForeignKey(MenuSection, related_name='items', on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to=user_directory_path,null=True)
    def __str__(self):
        return self.name
    
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_reserved=models.BooleanField(default=False)
    capacity=models.IntegerField(default=6)

    def __str__(self):
        return f"Table {self.number}"    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
   
    table = models.OneToOneField(Table, on_delete=models.CASCADE)
    
    

    def __str__(self):
        return f"Reservation by {self.name} for table {self.table.number}"    

class Order(models.Model):
    table_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = sum(item.quantity * item.menu_item.price for item in self.items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"