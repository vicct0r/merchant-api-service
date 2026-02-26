from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .. import models

User = get_user_model()
# os testes estão incompletos, este modulo é uma referência gerada por IA.
# fazer uma revisão com base no requisito real do projeto (business rules). 

class WorkplaceViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="uvictor@gmail.com",
            password="123"
        )

        self.user1 = User.objects.create_user(
            email="victor@gmail.com",
            password="123"
        )

        self.guest = User.objects.create_user(
            email="1guest@gmail.com",
            password="guest123330"
        )

        self.workplace = models.Workplace.objects.create(
            name="cGI-Enterprise-LTDA",
            cnpj="AA010-2330",
            owner=self.user
        )

    def test_authenticated_user_can_create_workplace(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "name": "wCGI-EnterpriseLTDA",
            "cnpj": "wwcgi-ent20100300-0001"
        }

        response = self.client.post(reverse('workplace:root'), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Workplace.objects.count(), 1 if not self.workplace else 2)
        self.assertEqual(models.Workplace.objects.filter(cnpj=data['cnpj']).first().owner, self.user1)
        self.assertEqual(models.Workplace.objects.filter(cnpj=data['cnpj']).first(), self.user1.workplace)

    def test_unauthenticated_user_cannot_create_workplace(self):
        
        data = {
            "name": "workplace-test-not-allowed",
            "cnpj": "invalid-anonymoususer-cnpj"
        }

        response = self.client.post(reverse('workplace:root'), data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(models.Workplace.objects.count(), 1 if self.workplace else 0)

    def test_workplace_member_can_invite_user(self):
        self.client.force_authenticate(user=self.user1)

        workplace_data = {
            "name": "workplace-test-allowed",
            "cnpj": "001-cnpj"
        }

        workplace_response = self.client.post(reverse('workplace:root'), workplace_data)

        data = {
            "user": self.guest.email
        }

        response = self.client.post(reverse('workplace:add_member'), data)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user1.workplace.whitelist.filter(pk=self.guest.pk).exists())

    def test_workplace_invite_n_accept_flow(self):
        self.client.force_authenticate(user=self.user1)

        workplace_data = {
            "name": "workplace-test-allowed",
            "cnpj": "001-cnpj"
        }

        workplace_response = self.client.post(reverse('workplace:root'), workplace_data)

        data = {
            "user": self.guest.email
        }

        response = self.client.post(reverse('workplace:add_member'), data)
        self.assertIn(response.status_code, [200, 201, 202])

        self.client.force_authenticate(user=self.guest)
        
        g_data = {
            "workplace_id": self.user1.workplace.id
        }

        guest_response = self.client.post(reverse('workplace:join'), data=g_data)
        self.assertIn(guest_response.status_code, [200, 201, 202])
        self.assertIn(self.guest, self.user1.workplace.whitelist.filter(id=self.guest.id))
        self.assertTrue(self.guest.workplace)
