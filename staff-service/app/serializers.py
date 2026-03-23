from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'name', 'role', 'email']
