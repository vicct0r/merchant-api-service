from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from clients.models import Client
from orders.serializers import OrderSerializer
from orders.models import Order

# fazer uma revisão neste modulo com base no modulo [test_views.py]
class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="123"
        )

        self.client = Client.objects.create(
            name="Client A",
            owner=self.user,
            phone="9999",
        )

    def test_owner_is_automatically_set_from_request(self):
        factory = APIRequestFactory()
        request = factory.post("/orders/")
        request.user = self.user

        data = {
            "client": self.client.id,
            "due_date": "18-02-2026 09:00",
            "status": "pending"
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save(owner=self.owner)

        self.assertEqual(order.client, self.client)
        self.assertEqual(order.status, Order.Status.PENDING)    
