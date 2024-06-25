from django.db import models
from authenticationSystem.models import CustomUserModel as User

# Create your models here.
class AccountModel(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    balance= models.DecimalField(max_digits= 10, decimal_places= 2, default= 0, blank= False, null= False)

    def make_PremiumUser(self):
            self.user.is_premium = True
            self.user.save()
            return 'Premium User'

    def __str__(self):
        return f'{self.user.username}'
    

choices= [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
status= [('success', 'Success'), ('failed', 'Failed')]
paymentMethod= [('mobile_money', 'Mobile Money')]

class PaymentChannels(models.Model):
    methods= models.CharField(max_length= 20, choices= paymentMethod, blank= False, null= False)
    name= models.CharField(max_length=100, blank= True)

    def save(self, *args, **kwargs):
        
        self.name = dict(paymentMethod).get(self.methods, self.methods)

        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.name}'
class TransactionModel(models.Model):
    account= models.ForeignKey(AccountModel, on_delete= models.CASCADE)
    amount= models.DecimalField(max_digits= 10, decimal_places= 2, blank= False, null= False)
    timestamp= models.DateTimeField(auto_now_add= True)
    transactionType= models.CharField(max_length= 10, choices= choices)
    transactionTypeStatus= models.CharField(max_length= 10, choices= status)
    transactionRefrence= models.CharField(max_length= 30, blank= False, null= False, default= None)
    paymentMethod= models.CharField(max_length= 20, blank= False, null= False)
    mobileNumber= models.CharField(max_length= 15, blank= False, null= False)
    carrier= models.CharField(max_length= 20, blank= False, null= False)

    def save(self, *args, **kwargs):
        self.paymentMethod = dict(paymentMethod).get(self.paymentMethod, self.paymentMethod)
        self.transactionType = dict(choices).get(self.transactionType, self.transactionType)
        self.transactionTypeStatus = dict(status).get(self.transactionTypeStatus, self.transactionTypeStatus)

        super().save(*args, **kwargs)
    
    def get_balance(self):
        return self.account.balance
    
    def process_transaction(self):
        if self.transactionType == 'deposit':
            self.account.balance = 0
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
    
class PaymentInfoModel(models.Model):
    account= models.ForeignKey(User, on_delete= models.CASCADE)
    firstName= models.CharField(max_length= 50, blank= False, null= False, default= '')
    lastName= models.CharField(max_length= 50, blank= False, null= False, default= '')
    email= models.CharField(default= '', max_length= 240)
    paymentMethod= models.CharField(max_length= 20, choices=paymentMethod, default=paymentMethod[0][0])
    paymentMethodName= models.CharField(max_length=100, blank= True)
    accountNumber= models.CharField(max_length= 15, blank= False, null= False)
    carrier= models.CharField(max_length= 20, blank= False, null= False)

    def save(self, *args, **kwargs):

        self.paymentMethodName = dict(paymentMethod).get(self.paymentMethod, self.paymentMethod)
        # self.firstName = self.account.first_name
        # self.lastName = self.account.last_name
        # self.email = self.account.email

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.account.username} ---> {self.paymentMethod} ---> {self.accountNumber} ---> {self.carrier}'
