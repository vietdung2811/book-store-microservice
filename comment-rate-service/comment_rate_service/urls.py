from django.urls import path
from app.views import ReviewListCreate

urlpatterns = [
    path('reviews/', ReviewListCreate.as_view()),
    path('reviews/<int:book_id>/', ReviewListCreate.as_view()),
]
