import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.



class Language(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
         return self.name


class Author(models.Model):

     first_name = models.CharField(max_length=100, help_text="Enter author first name")
     last_name = models.CharField(max_length=100, help_text="Enter author lastname")

     def __str__(self):
         return f'{self.first_name} {self.last_name}'

     def get_absolute_url(self):
         return reverse('author-detail', args=[str(self.id)])



class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:books-by-genre',
                        args=[self.slug])

    

class Book(models.Model):
    author = models.ForeignKey(Author,null=True,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True,default="Book")
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=20)
    available = models.BooleanField(default=True)
    click_count = models.IntegerField(default=0)
    order_count = models.IntegerField(default=0)
    
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
   
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])





#PascalCase C# camel_case python


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)