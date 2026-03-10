from django.urls import path
from app.views import StaffListCreate

urlpatterns = [
    path('staff/', StaffListCreate.as_view()),
]
