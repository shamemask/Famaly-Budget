from django.test import TestCase
from transactions.models import Client, Product, Transaction
from datetime import date, datetime
from decimal import Decimal

class ClientModelTest(TestCase):
    def test_client_creation(self):
        client = Client.objects.create(full_name="Иванова Анна Сергеевна", address="123456, г. Новгород, ул. Солнечная, д. 10, кв. 20")
        self.assertEqual(client.full_name, "Иванова Анна Сергеевна")
        self.assertEqual(client.address, "123456, г. Новгород, ул. Солнечная, д. 10, кв. 20")
        self.assertTrue(client.created_at)

class ProductModelTest(TestCase):
    def test_product_creation(self):
        client = Client.objects.create(full_name="Иванова Анна Сергеевна", address="Новгород")
        product = Product.objects.create(
            client=client,
            contract_date=date(2021, 5, 12),
            contract_number="1234567890",
            account_number="Не активирован"
        )
        self.assertEqual(product.contract_number, "1234567890")
        self.assertEqual(product.client, client)
        self.assertTrue(product.created_at)

class TransactionModelTest(TestCase):
    def test_transaction_creation(self):
        client = Client.objects.create(full_name="Иванова Анна Сергеевна", address="Новгород")
        product = Product.objects.create(
            client=client,
            contract_date=date(2021, 5, 12),
            contract_number="1234567890"
        )
        transaction = Transaction.objects.create(
            product=product,
            operation_datetime=datetime(2025, 4, 15, 14, 30),
            description_date=datetime(2025, 4, 15, 14, 31),
            amount=Decimal("-1500.00"),
            description="Оплата в ИП Сидоров В.В.",
            card_last_four="1234"
        )
        self.assertEqual(transaction.amount, Decimal("-1500.00"))
        self.assertEqual(transaction.product, product)
        self.assertEqual(transaction.card_last_four, "1234")
        self.assertTrue(transaction.created_at)
