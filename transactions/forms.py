from django import forms


class TransactionFileUploadForm(forms.Form):
    file = forms.FileField()
