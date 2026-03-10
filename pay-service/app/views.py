from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
import uuid

class PaymentCreate(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            payment.save()
            return Response(PaymentSerializer(payment).data)
        return Response(serializer.errors)

class PaymentList(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
