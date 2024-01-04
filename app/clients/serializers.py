from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'phone']