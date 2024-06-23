from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class AccountModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.user.username}'
choices= [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
class TransactionModel(models.Model):
    account= models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    amount= models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    timestamp= models.DateTimeField(auto_now_add=True)
    transactionType= models.CharField(max_length=10, choices= choices)

    def __str__(self):
        return f'{self.account.user.username} ---> {self.amount} ---> {self.timestamp} ---> {self.transactionType}'
