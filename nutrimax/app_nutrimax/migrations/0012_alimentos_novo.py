# Generated by Django 5.1 on 2024-11-24 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_nutrimax', '0011_delete_cardapio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alimentos_Novo',
            fields=[
                ('id_alimento', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField(max_length=255)),
                ('calorias', models.TextField(max_length=255)),
                ('carboidratos', models.TextField(max_length=255)),
                ('proteinas', models.TextField(max_length=255)),
                ('gorduras', models.TextField(max_length=255)),
            ],
        ),
    ]