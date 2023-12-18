from django.db import models
from django.contrib.auth.models import User
from loja.models import Produto

class ListaDesejos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produto.nome
    
    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total
    
    #usando classmethod para passar o user
    @classmethod
    def get_list_total(cls, user):
        itens_lista = ListaDesejos.objects.filter(user=user)
        # busca instancias do modelo ListaDesejos
        valor_total = sum([item.get_total for item in itens_lista])
        total_itens = sum([item.quantidade for item in itens_lista])
        return valor_total, total_itens
    
    @classmethod
    def get_total_qtd(cls, user):
        itens_lista = cls.objects.filter(user=user)
        #o cls aqui é uma referencia ao ListaDesejos
        total_quantidade = sum(item.quantidade for item in itens_lista if item.quantidade is not None)
        return total_quantidade
