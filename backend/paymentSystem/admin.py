from django.contrib import admin
from .models import AccountModel, TransactionModel

# Register your models here.
admin.site.register(AccountModel)
admin.site.register(TransactionModel)
