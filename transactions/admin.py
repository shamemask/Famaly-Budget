from django.contrib import admin
from .models import Client, Product, Transaction
from .forms import TransactionFileUploadForm
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .parser import parse_transaction_data


class TransactionAdmin(admin.ModelAdmin):
    change_list_template = "admin/transactions_upload.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload/",
                self.admin_site.admin_view(self.upload_file),
                name="transactions-upload",
            ),
        ]
        return custom_urls + urls

    def upload_file(self, request):
        if request.method == "POST":
            form = TransactionFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]
                content = file.read().decode("utf-8")
                parse_transaction_data(content)
                self.message_user(request, "Файл успешно загружен и обработан.")
                return HttpResponseRedirect("../")
        else:
            form = TransactionFileUploadForm()

        context = {
            "form": form,
            "title": "Загрузка файла транзакций",
            "app_label": self.model._meta.app_label,
            "opts": self.model._meta,
        }
        return render(request, "admin/upload_file.html", context)


admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Transaction, TransactionAdmin)
