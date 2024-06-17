from django.db import models

# Create your models here.

#Token model
class TokensModel(models.Model):
    token= models.CharField(blank=False, null=False, max_length= 999999999999)
    timestamp= models.DateTimeField(blank=False, null=False, auto_now_add= True)
    user_id= models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.user_id} ---> {self.timestamp}'