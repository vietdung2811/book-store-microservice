from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"

class CartCreate(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class AddCartItem(APIView):
    def post(self, request):
        book_id = request.data.get("book_id")
        try:
            r = requests.get(f"{BOOK_SERVICE_URL}/books/")
            books = r.json()
        except Exception:
            return Response({"error": "Could not connect to book-service"}, status=500)

        if not any(b["id"] == book_id for b in books):
            return Response({"error": "Book not found"}, status=404)
        
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ViewCart(APIView):
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

class UpdateCartItem(APIView):
    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
            serializer = CartItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

class DeleteCartItem(APIView):
    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
            item.delete()
            return Response({"message": "Item deleted"}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
