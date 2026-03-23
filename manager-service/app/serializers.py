from rest_framework import serializers
from .models import Manager

class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'name', 'department', 'email']
