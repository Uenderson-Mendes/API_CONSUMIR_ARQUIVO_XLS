from django.db import models



class Dados_existentes(models.Model):
    NIVEL = (
    ('F', 'F'),
    ('M', 'M'))

   # numero_usuario = models.CharField(max_length=90,null=True)
   # idU = models.CharField(max_length=150)
    nome = models.CharField('Nome Cadastrado:',max_length=100,null=True)
    sobrenome = models.CharField('Sobre Nome:',max_length=150, blank=True,null=True)
    sexo = models.CharField(max_length=1, choices=NIVEL, blank=False, null=False, default='M')
    altura = models.CharField(max_length=20,null=True)
    peso = models.CharField(max_length=20,null=True)
    nascimento= models.DateField(null=True)
    bairro = models.CharField(max_length=150,null=True)
    cidade = models.CharField(max_length=200,null=True)
    estado = models.CharField(max_length=200,null=True)
    numero = models.CharField('nome',max_length=30,null=True)

    def __str__(self):
        return self.nome
    objects = models.Manager()
