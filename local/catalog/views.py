
from .models import *
from .forms import *
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def index(request):
    book_count = Book.objects.all().count() #count(select * from Book)
    author_count = Author.objects.all().count()
    return render(
        request,
        'index.html',
        context={'book_count': book_count, 'author_count': author_count}
    )

@login_required(login_url='login/')
def book_list(request, category_slug=None):
    paginate_by = 4
    category = None
    categories = Category.objects.all()
    products = Book.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'catalog/book_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

    


@login_required(login_url='login/')
def contacts(request):
    return render(request, 'catalog/contacts.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(to='/catalog/profile/{}'.format(user.get_username()))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required(login_url='login/')
def custom_logout(request):
    logout(request)
    return redirect(to='/catalog/login/')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required(login_url='login/')
def profilePage(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'catalog/profile.html', {'profile': profile, 'user':user})
    
@login_required(login_url='login/')
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(to='/catalog/profile/{}'.format(request.user.get_username()))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'catalog/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

@login_required(login_url='login/')
def product_detail(request,id):
    product = get_object_or_404(Book,
                                    id=id)
    cart_product_form = CartAddProductForm()
    product.click_count += 1
    product.save()
    if product.stock == 0:
        product.available = False
        product.save()
    if request.method == 'POST':
        user_id = request.user
        count = request.POST.get("count")
        price = request.POST.get("price")
        if(product.stock >= int(count)):
            product.stock -= int(count)
            product.save()
        else:
            count = product.stock
        Cart.objects.create(user_id=user_id,book_id=product,count=count, total_price=int(count)*float(price))
        
        return render(request, 'catalog/book_detail.html', {'book': product,
                                                            'cart_product_form': cart_product_form})
    else:
        
        return render(request, 'catalog/book_detail.html', {'book': product,
                                                            'cart_product_form': cart_product_form})

@login_required(login_url='login/')  
def searchresult(request):
    query = request.GET.get('q')
    print(query)
    object_list = Book.objects.filter(Q(name__icontains=query) | Q(slug__icontains=query) | Q(category__name__icontains=query))
    return render(request, 'catalog/search_result.html', {'object_list':object_list})