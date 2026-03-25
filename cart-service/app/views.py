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
        customer_id = request.data.get("customer_id")
        book_id = request.data.get("book_id")
        quantity = request.data.get("quantity", 1)

        if not customer_id or not book_id:
            return Response({"error": "customer_id and book_id are required"}, status=400)

        # Find or create the cart for the customer
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)

        # Check if item already in cart, if so update quantity
        try:
            existing_item = CartItem.objects.get(cart=cart, book_id=book_id)
            existing_item.quantity += int(quantity)
            existing_item.save()
            serializer = CartItemSerializer(existing_item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            cart_item_data = {
                "cart": cart.id,
                "book_id": book_id,
                "quantity": quantity
            }
            serializer = CartItemSerializer(data=cart_item_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

class ViewCart(APIView):
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            
            # Fetch book details from book-service
            try:
                r = requests.get(f"{BOOK_SERVICE_URL}/books/", timeout=10)
                r.raise_for_status()
                books_data = r.json()
                books_map = {str(book['id']): book for book in books_data}
            except Exception as e:
                return Response({"error": f"Could not connect to book-service: {e}"}, status=500)

            # Combine cart items with book details
            enriched_items = []
            for item in items:
                book_details = books_map.get(str(item.book_id))
                if book_details:
                    enriched_items.append({
                        'id': item.id,
                        'quantity': item.quantity,
                        'book': book_details
                    })
            
            return Response(enriched_items)
            
        except Cart.DoesNotExist:
            # Return an empty list if the cart doesn't exist, which is not an error
            return Response([])

class DeleteCart(APIView):
    def delete(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            cart.delete()
            return Response({"message": "Cart deleted successfully"}, status=204)
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
