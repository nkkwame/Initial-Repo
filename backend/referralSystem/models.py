from django.db import models
from authenticationSystem.models import CustomUserModel as User

# Create your models here.
class ReferralModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    referral_code= models.CharField(max_length=8, unique= True)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} ---> {self.referral_code}'
