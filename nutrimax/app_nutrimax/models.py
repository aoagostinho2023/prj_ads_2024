from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    idade = models.IntegerField()
    sexo = models.TextField(max_length=255)
    atividade = models.TextField(max_length=255)
    altura = models.IntegerField()
    peso = models.IntegerField()
    objetivo = models.TextField(max_length=255)
    tmb = models.IntegerField()
    imc = models.IntegerField()
    imc_stat = models.TextField(max_length=255)