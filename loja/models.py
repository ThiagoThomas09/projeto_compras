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

