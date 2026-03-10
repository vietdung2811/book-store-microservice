from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Staff
from .serializers import StaffSerializer

class StaffListCreate(APIView):
    def get(self, request):
        staff_members = Staff.objects.all()
        serializer = StaffSerializer(staff_members, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
