from django.urls import path
from app.views import ShipmentCreate, ShipmentList

urlpatterns = [
    path('shipments/', ShipmentCreate.as_view()),
    path('shipments/list/', ShipmentList.as_view()),
]
