from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']
