from django.db import models


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract_date = models.DateField()
    contract_number = models.CharField(max_length=50, unique=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contract_number} - {self.client.full_name}"


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    operation_datetime = models.DateTimeField()
    description_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="RUB")
    description = models.TextField()
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_datetime} - {self.amount} {self.currency}"
