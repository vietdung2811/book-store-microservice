from django.urls import path
from django.views.generic.base import RedirectView
from .views import book_list, view_cart, staff_manage_books, checkout, add_to_cart

urlpatterns = [
    path('', RedirectView.as_view(url='books/', permanent=False)),
    path('books/', book_list, name='book_list'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/<int:customer_id>/', view_cart, name='view_cart'),
    path('manage/books/', staff_manage_books, name='staff_manage_books'),
    path('checkout/<int:customer_id>/', checkout, name='checkout'),
]
