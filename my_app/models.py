from django.db import models

class Transactions(models.Model):
    banco_origem = models.CharField(max_length= 50)
    agencia_origem = models.CharField(max_length= 20)
    conta_origem = models.CharField(max_length= 20)
    banco_destino = models.CharField(max_length= 50)
    agencia_destino = models.CharField(max_length= 20)
    conta_destino = models.CharField(max_length= 20)
    valor = models.FloatField()
    data_hora = models.DateTimeField()
    date_transactions = models.CharField(max_length= 10)


class History(models.Model):
    date_import = models.DateTimeField(auto_now = True)
    date_transactions = models.CharField(max_length = 10)
    user = models.CharField(max_length = 50)