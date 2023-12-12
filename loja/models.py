from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=150, null=True)

    def __str__(self):
        return self.nome

class Loja(models.Model):
    nome = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nome

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'static/images/default.jpg'
        return url
    
class Produto(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.FloatField()
    #Permitindo null temporariamente para migrar
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'static/images/default.jpg'
        return url


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
        valor_total = sum([item.get_total for item in itens_lista])
        total_itens = sum([item.quantidade for item in itens_lista])
        return valor_total, total_itens

