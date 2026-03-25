from django.urls import path
from app.views import OrderCreate, OrderDetail, CustomerOrderList

urlpatterns = [
    path('orders/', OrderCreate.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('orders/customer/<int:customer_id>/', CustomerOrderList.as_view()),
]
