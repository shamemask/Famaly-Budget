import re
from datetime import datetime
from decimal import Decimal
from .models import Client, Product, Transaction


def parse_transaction_data(content):
	# Извлечение информации о клиенте
	client_match = re.search(r'([А-Яа-я\s]+)\nАдрес места жительства: (.*?)\n', content)
	if client_match:
		full_name = client_match.group(1).strip()
		address = client_match.group(2).strip()
		client, _ = Client.objects.get_or_create(full_name=full_name, address=address)
	else:
		return

	# Извлечение информации о продукте
	contract_date_match = re.search(r'Дата заключения договора: (\d{2}\.\d{2}\.\d{4})', content)
	contract_number_match = re.search(r'Номер договора: (\d+)', content)
	account_number_match = re.search(r'Номер лицевого счета: (.*?)\n', content)

	contract_date = datetime.strptime(contract_date_match.group(1), '%d.%m.%Y').date() if contract_date_match else None
	contract_number = contract_number_match.group(1) if contract_number_match else None
	account_number = account_number_match.group(1).strip() if account_number_match else None

	if contract_number:
		product, _ = Product.objects.get_or_create(
			client=client,
			contract_date=contract_date,
			contract_number=contract_number,
			account_number=account_number
		)
	else:
		return

	# Извлечение транзакций
	transaction_lines = re.findall(
		r'(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2})\s+\|\s+(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2})\s+\|\s+([+-]?\d+\.\d{2}\s+P)\s+\|\s+([+-]?\d+\.\d{2}\s+P)\s+\|\s+(.+?)\s+\|\s+(\d{4}|-)\s+\|',
		content, re.MULTILINE
	)

	for line in transaction_lines:
		operation_datetime = datetime.strptime(line[0], '%d.%m.%Y %H:%M')
		description_date = datetime.strptime(line[1], '%d.%m.%Y %H:%M')
		amount = Decimal(line[2].replace(' P', '').replace(' ', ''))
		description = line[4].strip()
		card_last_four = line[5] if line[5] != '-' else None

		Transaction.objects.create(
			product=product,
			operation_datetime=operation_datetime,
			description_date=description_date,
			amount=amount,
			description=description,
			card_last_four=card_last_four
		)