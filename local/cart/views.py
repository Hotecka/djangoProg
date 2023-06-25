from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Book
from cart.models import Cart
from cart.models import Order
from django.contrib.auth.decorators import login_required
import datetime
from .forms import CartAddProductForm, OrderForm
# Create your views here.


@login_required(login_url='catalog:login')
def cart_detail(request):
    cart = Cart.objects.filter(user_id = request.user)
    sum = 0
    for item in cart:
        sum += item.total_price
    if request.method == "POST":
        id_dd = request.POST.get("product")
        item = Cart.objects.filter(id = id_dd)
        item.delete()
        return render(request, 'cart/detail.html', {'cart': cart, 'summary':sum})
    else:
        return render(request, 'cart/detail.html', {'cart': cart, 'summary':sum})
    
@login_required(login_url='catalog:login')
def order(request):
    cart = Cart.objects.filter(user_id = request.user)
    sum = 0
    form =  OrderForm(request.POST)
    for item in cart:
        sum += item.total_price
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            for item in cart:
                item.book_id.order_count += item.count
                item.book_id.save()
                item.delete()
            return redirect(to='/catalog/')
    else:
        return render(request, 'cart/order.html', {'cart': cart, 'summary':sum, 'form': form})