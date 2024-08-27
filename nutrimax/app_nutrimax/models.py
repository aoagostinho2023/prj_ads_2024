from django.db import models

# Create your models here.
class Usuario(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    ATIVIDADE_CHOICES = [
        ('alto', 'Alto'),
        ('medio', 'Médio'),
        ('baixo', 'Baixo'),
    ]
    
    OBJETIVO_CHOICES = [
        ('ganho', 'Ganho'),
        ('manter', 'Manter'),
        ('perda', 'Perda'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    atividade = models.CharField(max_length=5, choices=ATIVIDADE_CHOICES)
    altura = models.IntegerField()
    peso = models.IntegerField()
    objetivo = models.CharField(max_length=6, choices=OBJETIVO_CHOICES)
    tmb = models.IntegerField()
    imc = models.IntegerField()
    imc_stat = models.TextField(max_length=255)


class Alimentos(models.Model):
    id_alimento = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    calorias = models.TextField(max_length=255)
    carboidratos = models.TextField(max_length=255)
    proteinas = models.TextField(max_length=255)
    gorduras = models.TextField(max_length=255)
    