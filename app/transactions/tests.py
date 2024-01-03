from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from clients.models import Cliente
from .models import Transaccion
from .serializers import TransaccionSerializer

class TransaccionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.cliente = Cliente.objects.create(nombre_apellido='Jane Doe', correo_electronico='jane@example.com')

    def test_create_transaccion(self):
        data = {'cliente': self.cliente.id, 'imagen_frontside': 'front.jpg', 'imagen_backside': 'back.jpg', 'resultado': True}
        response = self.client.post('/transactions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaccion.objects.count(), 1)
        self.assertEqual(Transaccion.objects.get().cliente, self.cliente)