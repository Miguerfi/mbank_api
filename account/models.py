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
    cpf =  models.CharField(max_length=11,null=True,blank=True)
    nick = models.CharField(max_length=15)
    birthdate = models.DateField(null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    saldo = models.IntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "nick", "birthdate"]

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.nick


class Card(models.Model):
    card = models.IntegerField(blank=True, null=False)
    cvv = models.IntegerField(null=True, blank=True)
    exp_data = models.DateField(null=True, blank=True)
    cpf = models.ForeignKey(Account, on_delete=models.CASCADE)
