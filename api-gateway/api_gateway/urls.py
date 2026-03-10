from django.urls import path
from django.views.generic.base import RedirectView
from .views import book_list, view_cart, staff_manage_books, create_order

urlpatterns = [
    path('', RedirectView.as_view(url='books/', permanent=False)),
    path('books/', book_list, name='book_list'),
    path('cart/<int:customer_id>/', view_cart, name='view_cart'),
    path('manage/books/', staff_manage_books, name='staff_manage_books'),
    path('order/create/<int:customer_id>/', create_order, name='create_order'),
]
