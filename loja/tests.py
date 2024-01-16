from django.urls import reverse, resolve
from django.test import TestCase
from .models import Loja, Produto
from .views import loja

class TestUrls(TestCase):
    def test_list_url_is_resolved(self):
        url = reverse('loja')
        self.assertEqual(resolve(url).func, loja)

    def test_homepage(self):
        response = self.client.get(reverse('loja'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loja/loja.html')

class LojaTestCase(TestCase):
    def setUp(self):
        Loja.objects.create(nome='Loja Teste', image="teste_imagem.jpg")

    def test_loja_creation(self):
        loja = Loja.objects.get(nome="Loja Teste")
        self.assertEqual(loja.nome, "Loja Teste")
    
    def test_image(self):
        loja = Loja.objects.get(nome="Loja Teste")
        self.assertTrue(loja.imageURL.endswith("teste_imagem.jpg"))

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.loja = Loja.objects.create(
            nome='Produto Teste',
            image='imagem_produto.jpg'
        )

        Produto.objects.create(
            nome = 'Produto Teste', 
            preco = 10.0,
            loja = self.loja,
            image = 'imagem_produto.jpg'
        )
    
    def test_produto_creation(self):
        produto = Produto.objects.get(nome='Produto Teste')
        self.assertEqual(produto.nome, 'Produto Teste')
        self.assertEqual(produto.preco, 10.0)
        self.assertEqual(produto.loja, self.loja)
        self.assertTrue(produto.imageURL.endswith('imagem_produto.jpg'))