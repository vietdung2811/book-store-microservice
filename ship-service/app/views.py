from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Shipment
from .serializers import ShipmentSerializer
import uuid

class ShipmentCreate(APIView):
    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()
            shipment.tracking_number = f"TRK-{uuid.uuid4().hex[:8].upper()}"
            shipment.save()
            return Response(ShipmentSerializer(shipment).data)
        return Response(serializer.errors)

class ShipmentList(APIView):
    def get(self, request):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)
