from django.urls import path
from django.views.generic.base import RedirectView
from .views import book_list, view_cart, checkout, add_to_cart, login, logout, order_confirmation, delete_cart, my_orders

urlpatterns = [
    path('', RedirectView.as_view(url='books/', permanent=False)),
    path('books/', book_list, name='book_list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/<int:customer_id>/', view_cart, name='view_cart_id'),
    path('checkout/<int:customer_id>/', checkout, name='checkout'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
    path('my-orders/', my_orders, name='my_orders'),
    path('cart/delete/<int:customer_id>/', delete_cart, name='delete_cart'),
]

