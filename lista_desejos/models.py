from django.db import models
from django.contrib.auth.models import User
from loja.models import Produto

class ListaDesejos(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Lista de Desejos'

    def __str__(self):
        return self.nome if self.nome else 'Lista 1'
    
    def get_list_total(self):
        return sum(item.get_total for item in self.itens.all())
    
    def get_total_qtd(self):
        return sum(item.quantidade for item in self.itens.all() if item.quantidade)
    
    @classmethod
    def get_total_quantidade(cls, user):
        return sum(lista.get_total_qtd() for lista in cls.objects.filter(user=user))
    

class ItemListaDesejos(models.Model):
    lista = models.ForeignKey(ListaDesejos, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Itens da Lista de Desejos'

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}'
    
    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total
    

