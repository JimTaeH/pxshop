from django.contrib import admin
from .models import ShopOwner, Product, Buyer, Transaction

# Register your models here.
admin.site.register(ShopOwner)
admin.site.register(Product)
admin.site.register(Buyer)
admin.site.register(Transaction)