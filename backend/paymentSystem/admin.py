from django.contrib import admin
from .models import AccountModel, TransactionModel, PaymentChannels, PaymentInfoModel

# Register your models here.
admin.site.register(AccountModel)
admin.site.register(TransactionModel)
admin.site.register(PaymentChannels)
admin.site.register(PaymentInfoModel)
