from django.test import TestCase, Client as DjangoClient
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, MagicMock


class AdminUploadTest(TestCase):
    def setUp(self):
        self.client = DjangoClient()
        self.user = User.objects.create_superuser(
            username="admin", password="admin", email=""
        )
        self.client.login(username="admin", password="admin")
        self.sample_content = (
            "Иванова Анна Сергеевна\n"
            "Адрес места жительства: 123456, г. Новгород, ул. Солнечная, д. 10, кв. 20\n"
            "Дата заключения договора: 12.05.2021\n"
            "Номер договора: 1234567890\n"
            "Номер лицевого счета: Не активирован\n"
            "| 15.04.2025 14:30 | 15.04.2025 14:31 | -1500.00 P | -1500.00 P | Оплата в ИП Сидоров В.В. | 1234 |\n"
        )

    @patch("transactions.models.Client.objects")
    @patch("transactions.models.Product.objects")
    @patch("transactions.models.Transaction.objects")
    def test_upload_file(
        self, mock_transaction_objects, mock_product_objects, mock_client_objects
    ):
        # Моки для моделей
        mock_client = MagicMock()
        mock_client_objects.get_or_create.return_value = (mock_client, True)
        mock_product = MagicMock()
        mock_product_objects.get_or_create.return_value = (mock_product, True)
        mock_transaction = MagicMock()
        mock_transaction_objects.create.return_value = mock_transaction

        # Мок для парсера
        with patch("transactions.admin.parse_transaction_data") as mock_parse:
            mock_parse.return_value = None
            with open("test_file.txt", "w", encoding="utf-8") as f:
                f.write(self.sample_content)
            with open("test_file.txt", "rb") as f:
                response = self.client.post(
                    reverse("admin:transactions-upload"), {"file": f}
                )

        # Проверяем результат
        self.assertEqual(response.status_code, 302)  # Перенаправление после успеха
        mock_parse.assert_called_once_with(self.sample_content.replace("\n", "\r\n"))
        mock_client_objects.get_or_create.assert_called_once()
