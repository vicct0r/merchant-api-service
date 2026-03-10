from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .. import models
from merchants.models import Workplace

User = get_user_model()
# os testes estão incompletos, este modulo é uma referência gerada por IA.
# fazer uma revisão com base no requisito real do projeto (business rules). 

class WorkplaceViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="uvictor@gmail.com",
            password="123"
        )

        self.workplace = Workplace.objects.create(
            name="cGI-Enterprise-LTDA",
            cnpj="AA010-2330",
            owner=self.user
        )

        self.user.workplace = self.workplace

    def test_product_creation(self):
        self.client.force_authenticate(self.user)

        data = {
            "name": "test_product",
            "price": 2000.99,
            "quantity": 200,
            "sku": "AA0-IJ1-IUU"
        }

        response = self.client.post(reverse('products:root'), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Product.objects.last().workplace)
        self.assertEqual(models.Product.objects.last().workplace.owner, self.user)
