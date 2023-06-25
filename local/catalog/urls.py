from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.book_list, name='books'),
    path('books/<category_slug>/',views.book_list,name='books-by-genre'),
    path('edit/',views.edit, name='edit'),
    path('book/<id>/  ', views.product_detail, name='book-detail'),
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    path('profile/<str:username>/',views.profilePage,name='profile'),
    path('search/', views.searchresult, name='search_result'),
    path('logout/', views.custom_logout, name='logout'),
    path('contacts/', views.contacts, name='contacts')
    
    
    
]
# /?page=4 ? -> GET
