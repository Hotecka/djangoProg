from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    

admin.site.register(Book, ProductAdmin)      
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Profile,ProfileAdmin)

