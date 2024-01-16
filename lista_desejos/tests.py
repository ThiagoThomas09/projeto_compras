from django.urls import reverse, resolve
from django.test import Client, TestCase

from loja.models import Produto
from .views import wishlist, criar_lista, adicionar_a_lista_de_desejos
from django.contrib.auth.models import User
from .models import ItemListaDesejos, ListaDesejos

class URLTest(TestCase):
    def test_wishlist_url(self):
        url = reverse('wishlist')
        self.assertEqual(resolve(url).func, wishlist)

class ListaDesejosModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user test', password='123')
        ListaDesejos.objects.create(nome='Lista 1', user=self.user)

    def test_lista_creation(self):
        lista = ListaDesejos.objects.get(nome='Lista 1')
        self.assertEqual(lista.nome, 'Lista 1')
        self.assertEqual(lista.user, self.user)

class ItemListaDesejosModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user test', password='123')

        self.lista = ListaDesejos.objects.create(nome='Lista 1', user=self.user)

        self.produto = Produto.objects.create(nome='Produto Teste', preco=10.0)

    def test_item_lista_creation(self):
        item = ItemListaDesejos.objects.create(lista=self.lista, produto=self.produto, quantidade=2)
        self.assertEqual(item.lista, self.lista)
        self.assertEqual(item.produto, self.produto)
        self.assertEqual(item.quantidade, 2)   


class WishlistTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user test', password='123')
        self.client.login(username='user test', password='123')
    
    def test_wishlist_template(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loja/wishlist.html')

