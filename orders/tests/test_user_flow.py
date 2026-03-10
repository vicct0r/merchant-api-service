from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class OrderFlowTest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(email="victor@gmail.com", password="10000000VVVXXXX")
        self.employee = User.objects.create_user(email="mario@gmail.com", password="1000001999@")
        self.not_allowed_user = User.objects.create_user(email="wario@hotmail.com", password="10000000VVVXXXX")

    def test_workplace_creation(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(
            reverse('workplace:root'),
            data={"name": "workplace-001", "cnpj": "cnpj-001"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.owner.refresh_from_db()
        self.assertIsNotNone(self.owner.workplace)

    def test_employee_can_join_and_update_client(self):
        # Owner cria o workplace
        self.client.force_authenticate(self.owner)
        self.client.post(
            reverse('workplace:root'),
            data={"name": "workplace-001", "cnpj": "cnpj-001"}
        )
        self.owner.refresh_from_db()

        # Owner cria cliente
        client_response = self.client.post(
            reverse('clients:root'),
            data={"name": "Rafael M. Silva", "phone": "(44) 99102-9910", "observations": "dont call after 12"}
        )
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)
        client_id = client_response.data['id']

        # Owner convida employee
        invite_response = self.client.post(
            reverse('workplace:add_member'),
            data={"user": self.employee.email}
        )
        self.assertEqual(invite_response.status_code, status.HTTP_200_OK)

        # Employee aceita o convite
        self.client.force_authenticate(self.employee)
        join_response = self.client.post(
            reverse('workplace:join'),
            data={"workplace_id": str(self.owner.workplace.id)}
        )
        self.assertEqual(join_response.status_code, status.HTTP_200_OK)

        self.employee.refresh_from_db()
        self.assertIsNotNone(self.employee.workplace)

        # Employee atualiza o cliente
        update_response = self.client.patch(
            reverse('clients:retrieve', kwargs={'id': client_id}),
            data={"name": "João F. Mota Martins"}
        )
        self.assertIn(update_response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])
        self.assertEqual(update_response.data['name'], "João F. Mota Martins")
        
        self.client.force_authenticate(self.not_allowed_user)
        join_workplace_not_allowed_response = self.client.post(
            reverse('workplace:join'),
            data={"workplace_id": str(self.owner.workplace.id)}
        )
        
        self.assertNotIn(join_workplace_not_allowed_response.status_code, [200, 201, 202])
        self.assertEqual(join_workplace_not_allowed_response.status_code, 400)

        not_allowed_client_update = self.client.patch(
            reverse('clients:retrieve', kwargs={'id': client_id}),
            data={"name": "João F. Mota Martins"}
        )

        self.assertEqual(not_allowed_client_update.status_code, 400)