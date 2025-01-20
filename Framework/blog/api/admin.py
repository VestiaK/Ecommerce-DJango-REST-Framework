from django.contrib import admin
from .models import *



class ItemAdmin(admin.ModelAdmin):
    list_display=('name','description')

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)