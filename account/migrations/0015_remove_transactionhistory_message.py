# Generated by Django 4.1.7 on 2023-03-17 12:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0014_transactionhistory_message"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transactionhistory",
            name="message",
        ),
    ]
