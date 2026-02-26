from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clients.models import Client
from orders.models import Order

User = get_user_model()
# os testes estão incompletos, este modulo é uma referência gerada por IA.
# fazer uma revisão com base no requisito real do projeto (business rules). 

class OrderViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="uvictor@gmail.com",
            password="123"
        )

        self.client_obj = Client.objects.create(
            name="Client A",
            owner=self.user,
            phone="9999",
        )

    def test_authenticated_user_can_create_order(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "client": self.client_obj.id,
            "due_date": "18-02-2026 09:00",
            "status": "pending"
        }

        response = self.client.post("v1/orders/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().owner, self.user)

    def test_unauthenticated_user_cannot_create_order(self):
        data = {
            "client": self.client_obj.id,
            "due_date": "18-02-2026 09:00",
            "status": "pending"
        }

        response = self.client.post("/orders/", data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), 0)
