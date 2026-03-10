from django.urls import path
from app.views import ManagerListCreate

urlpatterns = [
    path('managers/', ManagerListCreate.as_view()),
]
