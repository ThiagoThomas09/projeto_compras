from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=150, null=True)

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.FloatField()

    def __str__(self):
        return self.nome

class ListaDesejos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produto.nome

