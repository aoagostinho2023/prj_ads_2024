# Generated by Django 5.1 on 2024-11-24 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_nutrimax', '0008_remove_cardapio_alimentos_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cardapio',
        ),
    ]
