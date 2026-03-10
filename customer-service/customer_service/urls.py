from django.urls import path
from app.views import CustomerListCreate

urlpatterns = [
    path('customers/', CustomerListCreate.as_view()),
]
