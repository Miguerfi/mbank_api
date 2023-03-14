from django.contrib import admin
from account.models import Account
from account.models import Card
from account.models import Balance
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Balance)

