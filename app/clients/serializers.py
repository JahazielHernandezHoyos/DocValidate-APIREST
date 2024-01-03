from rest_framework import serializers
from .models import Clients

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id', 'full_name', 'email', 'phone']

class ClientsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['full_name', 'email', 'phone']
