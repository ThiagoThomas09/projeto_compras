# Generated by Django 5.0 on 2024-01-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0007_alter_carrinho_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='email_enviado',
            field=models.BooleanField(default=False),
        ),
    ]