from django.urls import path
from app.views import CartCreate, AddCartItem, ViewCart, UpdateCartItem, DeleteCartItem, DeleteCart

urlpatterns = [
    path('carts/', CartCreate.as_view()),
    path('cart-items/', AddCartItem.as_view()),
    path('carts/<int:customer_id>/', ViewCart.as_view()),
    path('carts/<int:customer_id>/delete/', DeleteCart.as_view()), # New URL pattern
    path('cart-items/<int:pk>/', UpdateCartItem.as_view()),
    path('cart-items/<int:pk>/delete/', DeleteCartItem.as_view()),
]
