from rest_framework.test import APITestCase
from rest_framework import status


class ClientAPITest(APITestCase):
    fixtures = ["test_data.json"]

    def test_list_clients(self):
        response = self.client.get("/api/clients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["full_name"], "Иванова Анна Сергеевна")


class ProductAPITest(APITestCase):
    fixtures = ["test_data.json"]

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["contract_number"], "1234567890")


class TransactionAPITest(APITestCase):
    fixtures = ["test_data.json"]

    def test_list_transactions(self):
        response = self.client.get("/api/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(float(response.data[0]["amount"]), -1500.00)
