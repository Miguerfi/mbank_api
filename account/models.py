from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class AccountManager(BaseUserManager):
    def create_user(
        self,
        email,
        full_name=None,
        nick=None,
        birthdate=None,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("O email deve ser definido")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            nick=nick,
            birthdate=birthdate,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password=password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=60, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    nick = models.CharField(max_length=15)
    birthdate = models.DateField(null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "nick", "birthdate"]

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.nick


class Balance(models.Model):
    cpf = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    saldo = models.FloatField(default=0, blank=True, null=True)
    saved_money = models.FloatField(default=0, blank=True, null=True)
    money_applied = models.FloatField(default=0, blank=True, null=True)


class Card(models.Model):
    GOLD = "gl"
    PLATINUM = "pt"
    DIAMOND = "dm"

    TYPE_CARD_CHOICES = [(GOLD, "Gold"), (PLATINUM, "Platinum"), (DIAMOND, "Diamond")]
    card = models.IntegerField(blank=True, null=True)
    cvv = models.IntegerField(null=True, blank=True)
    exp_data = models.DateField(null=True, blank=True)
    type_card = models.CharField(max_length=2, choices=TYPE_CARD_CHOICES, default=GOLD)
    cpf = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE)


class TransactionHistory(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_id = models.CharField(max_length=32, null=True, blank=True)
    message = models.CharField(max_length=60, null=True, blank=True)


class TransactionAuthor(models.Model):
    author = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey(
        TransactionHistory, related_name="author_transaction", on_delete=models.CASCADE
    )


class TransactionTarget(models.Model):
    target = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey(
        TransactionHistory, related_name="target_transaction", on_delete=models.CASCADE
    )
