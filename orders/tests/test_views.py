from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clients.models import Client
from orders.models import Order
from django.urls import reverse
from merchants.models import Workplace
from products.models import Product
from django.utils import timezone

User = get_user_model()
# os testes estão incompletos, este modulo é uma referência gerada por IA.
# fazer uma revisão com base no requisito real do projeto (business rules). 

class OrderViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="victor@gmail.com",
            password="123"
        )

        self.workplace = Workplace.objects.create(
            name="workplace-test-01",
            cnpj="workplace01",
            owner=self.user
        )

        self.user.workplace = self.workplace

        self.cliente = Client.objects.create(
            name="Test Client",
            workplace=self.workplace,
            phone="9999",
        )

        self.product = Product.objects.create(
            name="MotherBoard Asus TUF Gaming PLUS III",
            price=2000.99,
            quantity=200,
            sku="AA002-30009",
            workplace=self.workplace
        )
        self.product.workplace = self.workplace

    def test_cliente_creation_workplace(self):
        self.client.force_authenticate(self.user)
        
        cliente_data = {
            "name": "picapeue",
            "phone": "0000001",
            "observations": "he likes to know about details on the process."
        }

        cliente_response = self.client.post(reverse('clients:root'), data=cliente_data)

        self.assertEqual(cliente_response.status_code, 201)

        data = {
            "client": cliente_response.json()['id'],
            "due_date": "20-04-2026 06:00",
            "status": "pending"
        }

        response = self.client.post(reverse('orders:root'), data=data)

        self.assertIn(response.status_code, [200, 201, 202])

        p_data = {
            "product": self.product.id,
            "quantity": 20000,
        }

        order_response = self.client.post(reverse('orders:add_product', kwargs={'order_id': response.json()['id']}), data=p_data)

        self.assertEqual(order_response.status_code, 200)
        self.assertTrue(order_response.json()['message'])