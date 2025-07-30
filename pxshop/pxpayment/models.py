from django.db import models
import uuid

class ShopOwner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Add more fields as needed (e.g. phone, address, etc.)

    def __str__(self):
        return self.name
    
# Create your models here.
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    productName = models.CharField(max_length=255)
    productDes = models.TextField(max_length=5000)
    price = models.FloatField()
    # sold_units = models.IntegerField()
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.productName} {self.shop_owner.name}"
    
class Buyer(models.Model):
    user_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    generation = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.generation} {self.firstname} {self.surname}"
    
class TransactionItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total_price = models.FloatField(default=0.0)

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    # product = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item_list = models.ManyToManyField(TransactionItems)
    subtotal = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.transaction_id}"

