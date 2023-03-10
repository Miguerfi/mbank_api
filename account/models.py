from django.db import models


class Account(models.Model):
    full_name = models.CharField(max_length=60, null=True, blank=True)
    cpf = models.IntegerField(blank=True,null=True)
    nick = models.CharField(max_length=15)
    birthdate = models.DateField(null=False)
    password = models.CharField(max_length=60,null=True,blank=True)
class Card(models.Model):
    card = models.IntegerField(blank=True,null=False)
    cvv = models.IntegerField(null=True,blank=True)
    exp_data = models.DateField(null=True,blank=True)
    cpf = models.ForeignKey(Account,on_delete=models.CASCADE)

