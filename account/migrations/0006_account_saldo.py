# Generated by Django 4.1.7 on 2023-03-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_account_cpf"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="saldo",
            field=models.IntegerField(default=0),
        ),
    ]
