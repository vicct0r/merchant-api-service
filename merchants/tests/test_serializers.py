from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from .. import models, serializers

User = get_user_model()


class WorkplaceSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="teste@example.com",
            password="test@123"
        )

    def test_workplace_creation(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('workplace:root'))
        request.user = self.user

        data = {
            "name": "workplace-00",
            "cnpj": "AA-20-23"
        }

        serializer = serializers.WorkplaceSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
