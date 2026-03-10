from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"

class CategoryListCreate(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CatalogOverview(APIView):
    def get(self, request):
        # High level overview: categories and books
        try:
            r = requests.get(f"{BOOK_SERVICE_URL}/books/")
            books = r.json()
        except Exception:
            books = []
        
        categories = Category.objects.all()
        cat_serializer = CategorySerializer(categories, many=True)
        
        return Response({
            "categories": cat_serializer.data,
            "total_books": len(books),
            "books_preview": books[:5]
        })
