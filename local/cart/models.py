from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book
import datetime

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE) 
    count = models.IntegerField()
    total_price = models.FloatField()
    
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=300)
    datetime = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    