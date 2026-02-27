from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.urls import reverse

from clients.models import Client
from orders.serializers import OrderSerializer
from orders.models import Order
from merchants.models import Workplace

User = get_user_model()
# fazer uma revisão neste modulo com base no modulo [test_views.py]
class OrderSerializerTest(TestCase):

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

        self._client = Client.objects.create(
            name="Test Client",
            workplace=self.workplace,
            phone="9999",
        )

