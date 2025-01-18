from django.contrib import admin
from .models import Item



class ItemAdmin(admin.ModelAdmin):
    list_display=('name','description')

# Register your models here.
admin.site.register(Item,ItemAdmin)