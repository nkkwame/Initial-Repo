from django.db import models
from authenticationSystem.models import CustomUserModel as User

# Create your models here.
class AccountModel(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    balance= models.DecimalField(max_digits= 10, decimal_places= 2, default= 0, blank= False, null= False)

    def is_PremiumUser(self):
        if self.balance >= 30:
            self.user.is_premium = True
            self.user.save()
            return 'Premium User'
        else:
            self.user.is_premium = False
            return 'Non-Premium User'

    def __str__(self):
        return f'{self.user.username}'
    

choices= [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
status= [('success', 'Success'), ('failed', 'Failed')]
class TransactionModel(models.Model):
    account= models.ForeignKey(AccountModel, on_delete= models.CASCADE)
    amount= models.DecimalField(max_digits= 10, decimal_places= 2, blank= False, null= False)
    timestamp= models.DateTimeField(auto_now_add= True)
    transactionType= models.CharField(max_length= 10, choices= choices)
    transactionTypeStatus= models.CharField(max_length= 10, choices= status)
    transactionRefrence= models.CharField(max_length= 30, blank= False, null= False, default= None)
    
    def get_balance(self):
        return self.account.balance
    
    def process_transaction(self):
        if self.transactionType == 'deposit':
            self.account.balance += self.amount
            self.account.save()
        elif self.transactionType == 'withdrawal':
            if self.account.balance >= self.amount:
                self.account.balance -= self.amount
                self.account.save()
            else:
                self.transactionTypeStatus = 'failed'
        self.save()
        return self.transactionTypeStatus

    def __str__(self):
        return f'{self.account.user.username} ---> {self.amount} ---> {self.timestamp} ---> {self.transactionType}'
