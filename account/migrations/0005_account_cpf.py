# Generated by Django 4.1.7 on 2023-03-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "account",
            "0004_remove_account_cpf_account_date_joined_account_email_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="cpf",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]