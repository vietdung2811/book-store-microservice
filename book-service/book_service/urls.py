from django.urls import path
from app.views import BookListCreate

urlpatterns = [
    path('books/', BookListCreate.as_view()),
]
