from django.contrib import admin
from .models import MenuSection,MenuItem,Table,Reservation,Order,OrderItem

# Register your models here.
admin.site.register(MenuSection)
admin.site.register(Table)
admin.site.register(Reservation)

admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
