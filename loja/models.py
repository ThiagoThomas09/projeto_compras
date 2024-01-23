from django.db import models
from django.contrib.auth.models import User

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

class Carrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status_aberto = models.BooleanField(default=True)
    email_enviado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Carrinhos de Compras"

    def __str__(self):
        return f"Carrinho de {self.user.username}"

    @property
    def get_total(self):
        return sum(item.get_total for item in self.cart_items.all())

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='cart_items', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} de {self.produto.nome}"

    @property
    def get_total(self):
        return self.produto.preco * self.quantidade
