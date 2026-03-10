from django.urls import path
from app.views import OrderCreate, OrderDetail

urlpatterns = [
    path('orders/', OrderCreate.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
]
