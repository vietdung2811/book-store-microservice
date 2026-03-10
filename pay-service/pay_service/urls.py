from django.urls import path
from app.views import PaymentCreate, PaymentList

urlpatterns = [
    path('payments/', PaymentCreate.as_view()),
    path('payments/list/', PaymentList.as_view()),
]
