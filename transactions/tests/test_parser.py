from django.test import TestCase
from unittest.mock import patch, MagicMock
from datetime import datetime
from decimal import Decimal


class ParserTest(TestCase):
    def setUp(self):
        self.sample_content = (
            "Иванова Анна Сергеевна\n"
            "Адрес места жительства: 123456, г. Новгород, ул. Солнечная, д. 10, кв. 20\n"
            "Дата заключения договора: 12.05.2021\n"
            "Номер договора: 1234567890\n"
            "Номер лицевого счета: Не активирован\n"
            "| 15.04.2025 14:30 | 15.04.2025 14:31 | -1500.00 P | -1500.00 P | Оплата в ИП Сидоров В.В. | 1234 |\n"
            "| 15.04.2025 10:15 | 15.04.2025 10:16 | +2500.00 P | +2500.00 P | Внутрибанковский перевод с договора 9876543210 | 1234 |\n"
        )

    @patch("transactions.models.Client.objects")
    @patch("transactions.models.Product.objects")
    @patch("transactions.models.Transaction.objects")
    def test_parse_client(
        self, mock_transaction_objects, mock_product_objects, mock_client_objects
    ):
        # Мок для клиента
        mock_client = MagicMock()
        mock_client.full_name = "Иванова Анна Сергеевна"
        mock_client.address = "123456, г. Новгород, ул. Солнечная, д. 10, кв. 20"
        mock_client_objects.get_or_create.return_value = (mock_client, True)

        # Мок для продукта (чтобы парсер прошел)
        mock_product = MagicMock()
        mock_product_objects.get_or_create.return_value = (mock_product, True)

        # Вызываем парсер
        from transactions.parser import parse_transaction_data

        parse_transaction_data(self.sample_content)

        # Проверяем, что get_or_create для клиента вызван правильно
        mock_client_objects.get_or_create.assert_called_once_with(
            full_name="Иванова Анна Сергеевна",
            address="123456, г. Новгород, ул. Солнечная, д. 10, кв. 20",
        )

    @patch("transactions.models.Client.objects")
    @patch("transactions.models.Product.objects")
    @patch("transactions.models.Transaction.objects")
    def test_parse_product(
        self, mock_transaction_objects, mock_product_objects, mock_client_objects
    ):
        # Мок для клиента
        mock_client = MagicMock()
        mock_client_objects.get_or_create.return_value = (mock_client, True)

        # Мок для продукта
        mock_product = MagicMock()
        mock_product.contract_number = "1234567890"
        mock_product.contract_date = datetime(2021, 5, 12).date()
        mock_product.account_number = "Не активирован"
        mock_product_objects.get_or_create.return_value = (mock_product, True)

        # Вызываем парсер
        from transactions.parser import parse_transaction_data

        parse_transaction_data(self.sample_content)

        # Проверяем, что get_or_create для продукта вызван правильно
        mock_product_objects.get_or_create.assert_called_once_with(
            client=mock_client,
            contract_date=datetime(2021, 5, 12).date(),
            contract_number="1234567890",
            account_number="Не активирован",
        )

    @patch("transactions.models.Client.objects")
    @patch("transactions.models.Product.objects")
    @patch("transactions.models.Transaction.objects")
    def test_parse_transactions(
        self, mock_transaction_objects, mock_product_objects, mock_client_objects
    ):
        # Мок для клиента
        mock_client = MagicMock()
        mock_client_objects.get_or_create.return_value = (mock_client, True)

        # Мок для продукта
        mock_product = MagicMock()
        mock_product_objects.get_or_create.return_value = (mock_product, True)

        # Мок для транзакций
        mock_transaction = MagicMock()
        mock_transaction_objects.create.return_value = mock_transaction

        # Вызываем парсер
        from transactions.parser import parse_transaction_data

        parse_transaction_data(self.sample_content)

        # Проверяем, что create для транзакций вызван дважды
        self.assertEqual(mock_transaction_objects.create.call_count, 2)
        mock_transaction_objects.create.assert_any_call(
            product=mock_product,
            operation_datetime=datetime(2025, 4, 15, 14, 30),
            description_date=datetime(2025, 4, 15, 14, 31),
            amount=Decimal("-1500.00"),
            description="Оплата в ИП Сидоров В.В.",
            card_last_four="1234",
        )
        mock_transaction_objects.create.assert_any_call(
            product=mock_product,
            operation_datetime=datetime(2025, 4, 15, 10, 15),
            description_date=datetime(2025, 4, 15, 10, 16),
            amount=Decimal("2500.00"),
            description="Внутрибанковский перевод с договора 9876543210",
            card_last_four="1234",
        )
