from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
import requests

PAY_SERVICE_URL = "http://pay-service:8000"
SHIP_SERVICE_URL = "http://ship-service:8000"

from rest_framework import status

class OrderCreate(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Trigger payment
            try:
                requests.post(f"{PAY_SERVICE_URL}/payments/", json={
                    "order_id": order.id,
                    "amount": float(order.total_amount)
                })
            except Exception:
                pass
                
            # Trigger shipping
            try:
                requests.post(f"{SHIP_SERVICE_URL}/shipments/", json={
                    "order_id": order.id,
                    "customer_id": order.customer_id
                })
            except Exception:
                pass

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
