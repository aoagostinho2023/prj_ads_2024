# Generated by Django 5.1 on 2024-08-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_nutrimax', '0005_alter_usuario_atividade_alter_usuario_objetivo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alimentos',
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
